# Hướng dẫn chạy project 
- B1: Chạy toàn bộ input để ra kết quả bằng cách run lệnh sau:

```bash
    python ./main.py
```

- B2: Để sử dụng GUI hiển thị:

```bash
    python ./GUI.py
```
- Cách sử dụng GUI
    - Sử dụng phím mũi tên trái phải để chọn input.
    - Click chọn thuật toán để bắt đầu.
    - Click nút Start/Pause để dừng thuật toán.
    - Click nút Reset để hiển thị lại từ đầu quá trình.

***Ghi chú***:
- Nếu không muốn chạy lại toàn bộ thuật toán (thời gian lâu) thì có thể sử dụng luôn kết quả nhóm đã chạy được (B2).
- `BFS.py`, `DFS.py`,... là tên các thuật toán.
- `utils.py` chứa các hàm bổ trợ cho thuật toán
- `node.py` định nghĩa 2 class node và maze
- `main.py` để chạy thuật toán và viết kết quả của các input vào file output
- Folder `inputs` chứa bộ 11 bộ input gồm 9 bộ có kết quả và 2 bộ không có kết quả (10, 11)
- Folder `outputs` chứa kết ouput theo yêu cầu của project
- Folder `outputs-for-gui` kết quả của từng thuật toán hiển thị GUI.