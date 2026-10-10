import base64
import flet as ft

def main(page: ft.Page):
    page.title = "Flet Web Image Preview"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 画像プレビュー用コントロール
    img = ft.Image(
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
        border_radius=ft.border_radius.all(10),
    )

    # ステータス表示
    status_text = ft.Text("画像を選択してください", color=ft.colors.GREY_700)

    # ファイル選択時の処理（Web対応）
    def on_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            # Webの場合は e.files[0].base64 に画像のバイトデータ（Base64エンコード済み）が入る
            file_info = e.files[0]
            if file_info.base64:
                # Base64データをImageのsrcに直接流し込む
                img.src_base64 = file_info.base64
                img.update()
                status_text.value = f"選択されたファイル: {file_info.name}"
                status_text.update()
            else:
                status_text.value = "画像の読み込みに失敗しました"
                status_text.update()

    # ファイルピッカーの作成（include_base64=True がWebでは重要）
    file_picker = ft.FilePicker(on_result=on_file_picker_result)
    page.overlay.append(file_picker)

    # ボタン
    upload_button = ft.ElevatedButton(
        "画像を選択",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"],
            include_base64=True, # ★Webでプレビューするために必須
        ),
    )

    page.add(
        ft.Column(
            [
                ft.Text("Web画像アップロード & プレビュー", size=20, weight=ft.FontWeight.BOLD),
                img,
                upload_button,
                status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

# Webとして起動する場合、ポートやアップロードディレクトリの指定が必要な場合があります
# ローカルでWebテストをする場合: flet run main.py -d (または通常の `flet run`)
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
