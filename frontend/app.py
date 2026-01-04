import streamlit as st
import requests

st.set_page_config(page_title="ToDo App", layout="centered")

# --- Authentication ---
if "jwt_token" not in st.session_state:
    st.title("Login")
    username = st.text_input("Логин", key="username_l").strip()
    password = st.text_input("Пароль", type="password", key="password_l").strip()

    if st.button("Войти"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state["jwt_token"] = data.get("access_token")
                st.success("Вход выполнен!")
            else:
                st.error("Ошибка логина")
        except requests.exceptions.RequestException as e:
            st.error(f"Ошибка подключения к серверу: {e}")

    st.title("Registration")
    username_r = st.text_input("Логин", key="username_r")
    email_r = st.text_input("Email", key="email_r")
    password_r = st.text_input("Пароль", type="password", key="password_r")

    if st.button("Зарегистрироваться", key="register_button"):
        response = requests.post(
            "http://127.0.0.1:8000/users",
            json={"username": username_r, "email": email_r, "password": password_r}
        )
        if response.content:
            try:
                result = response.json()
                if response.status_code in [200, 201]:
                    st.success("Регистрация успешна!")
                else:
                    st.error(result.get("error", "Ошибка регистрации"))
            except ValueError:
                st.error(f"Невалидный JSON от сервера: {response.text}")
        else:
            st.error(f"Сервер не вернул данных. Код ответа: {response.status_code}")

# --- Dashboard ---
else:
    st.title("Dashboard")
    st.write("Добро пожаловать в ваш ToDo лист!")

    headers = {
        "Authorization": f"Bearer {st.session_state['jwt_token']}"
    }

    task_title = st.text_input("Название задачи", key="task_title")
    task_description = st.text_area("Описание задачи", key="task_description")

    if st.button("Добавить задачу"):
        if not task_title.strip():
            st.warning("Введите название задачи!")
        else:
            response = requests.post(
                "http://127.0.0.1:8000/todos/",
                json={
                    "title": task_title,
                    "description": task_description
                },
                headers=headers
            )
            if response.status_code in [200, 201]:
                st.success("Задача добавлена!")
            else:
                try:
                    st.error(response.json().get("error", "Ошибка при добавлении задачи"))
                except ValueError:
                    st.error(f"Ошибка: {response.text}")

    if st.button("Показать все задачи") or "show_tasks" not in st.session_state:
        response = requests.get(
            "http://127.0.0.1:8000/todos/",
            headers=headers
        )
        if response.status_code == 200:
            st.session_state["todos"] = response.json()
            st.session_state["show_tasks"] = True
        else:
            st.error("Не удалось загрузить задачи")
            st.session_state["todos"] = []

    if st.session_state.get("show_tasks", False):
        todos = st.session_state.get("todos", [])
        if not todos:
            st.info("Задач пока нет")
        else:
            st.subheader("Все задачи")
            for todo in todos:
                st.markdown("---")

                new_title = st.text_input(
                    "Название",
                    value=todo["title"],
                    key=f"title_{todo['id']}"
                )

                new_description = st.text_area(
                    "Описание",
                    value=todo.get("description", ""),
                    key=f"desc_{todo['id']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Сохранить", key=f"save_{todo['id']}"):
                        update_response = requests.put(
                            f"http://127.0.0.1:8000/todos/{todo['id']}",
                            headers=headers,
                            json={
                                "title": new_title,
                                "description": new_description
                            }
                        )
                        if update_response.status_code == 200:
                            st.success("Задача обновлена")
                            response = requests.get(
                                "http://127.0.0.1:8000/todos/",
                                headers=headers
                            )
                            if response.status_code == 200:
                                st.session_state["todos"] = response.json()
                                st.rerun()
                        else:
                            st.error("Ошибка при обновлении задачи")

                with col2:
                    if st.button("Удалить", key=f"delete_{todo['id']}"):
                        del_response = requests.delete(
                            f"http://127.0.0.1:8000/todos/{todo['id']}",
                            headers=headers
                        )
                        if del_response.status_code == 200:
                            st.success("Задача удалена")
                            response = requests.get(
                                "http://127.0.0.1:8000/todos/",
                                headers=headers
                            )
                            if response.status_code == 200:
                                st.session_state["todos"] = response.json()
                                st.rerun()
                        else:
                            st.error("Ошибка при удалении задачи")
                            
                            
    st.markdown("---")
    st.subheader("Опасная зона ⚠️")

    if st.button("Удалить аккаунт", type="primary"):
        response = requests.delete(
            "http://127.0.0.1:8000/users/",
            headers=headers
        )

        if response.status_code == 200:
            st.success("Аккаунт удалён")
            st.session_state.clear()   
            st.rerun()
        else:
            try:
                st.error(response.json().get("detail", "Ошибка удаления аккаунта"))
            except ValueError:
                st.error("Ошибка сервера")