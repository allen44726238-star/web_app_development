from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理註冊邏輯與頁面渲染。
    GET: 顯示註冊表單。
    POST: 接收資料建立新帳號，成功後導向登入頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理登入邏輯與頁面渲染。
    GET: 顯示登入表單。
    POST: 驗證帳號密碼，成功後記錄 Session 並導向首頁。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    執行登出，清除 Session 紀錄，並導回首頁。
    """
    pass
