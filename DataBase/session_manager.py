def create_session_manager():
    _current_user_session = {}

    def set_user_session(user_id, user_role):
        """Устанавливает текущую сессию пользователя."""
        _current_user_session['user_id'] = user_id
        _current_user_session['user_role'] = user_role

    def get_user_session():
        """Возвращает данные текущей сессии пользователя."""
        return _current_user_session

    def clear_user_session():
        """Очищает текущую сессию пользователя."""
        _current_user_session.clear()

    return set_user_session, get_user_session, clear_user_session


set_user_session, get_user_session, clear_user_session = create_session_manager()
