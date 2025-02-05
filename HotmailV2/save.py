import os

def read_and_save_files(directory_path, output_file_path):
    # Kiểm tra xem đường dẫn đến thư mục có tồn tại hay không
    if not os.path.exists(directory_path):
        print(f"Thư mục {directory_path} không tồn tại.")
        return

    # Mở file output để ghi nội dung vào
    with open(output_file_path, 'w') as output_file:
        # Lặp qua tất cả các tệp trong thư mục
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # Kiểm tra nếu là tệp văn bản
            if filename.endswith(".txt") and os.path.isfile(file_path):
                # Mở và đọc nội dung từ tệp và ghi vào file output
                with open(file_path, 'r') as input_file:
                    content = input_file.read()
                    output_file.write(content + '\n')  # Ghi nội dung vào file output, cách nhau bởi dấu xuống dòng

    print(f"Nội dung của các tệp trong thư mục đã được ghi vào {output_file_path}.")

# Sử dụng hàm với đường dẫn thư mục và đường dẫn file output của bạn
read_and_save_files("SUCCESS", "MAILOK.txt")

