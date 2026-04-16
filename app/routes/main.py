from flask import Blueprint, render_template, request, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    處理首頁，檢查是否登入，並顯示每日簡易運勢（如適用）。
    輸出: 渲染 'index.html'。
    """
    pass

@main_bp.route('/fortune', methods=['GET'])
def fortune_index():
    """
    顯示抽籤儀式頁面，提供搖籤筒畫面。
    輸出: 渲染 'fortune/index.html'。
    """
    pass

@main_bp.route('/fortune/draw', methods=['POST'])
def fortune_draw():
    """
    執行抽籤動作。
    隨機挑選一張籤詩，若有登入則儲存至 History，
    最後重導向至結果頁 `/fortune/result/<fortune_id>`。
    """
    pass

@main_bp.route('/fortune/result/<int:fortune_id>', methods=['GET'])
def fortune_result(fortune_id):
    """
    顯示單一籤詩的詳細解說內容。
    若 ID 不存在需處理 404。
    輸出: 渲染 'fortune/result.html' 帶入籤詩資料。
    """
    pass

@main_bp.route('/history', methods=['GET'])
def history_index():
    """
    取得使用者的所有抽籤紀錄並顯示清單。
    若未登入需導向登入頁面。
    輸出: 渲染 'history/index.html'。
    """
    pass

@main_bp.route('/donate', methods=['GET'])
def donate_index():
    """
    顯示香油錢捐款與贊助資訊。
    輸出: 渲染 'donate/index.html'。
    """
    pass
