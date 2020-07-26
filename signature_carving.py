# Case List
#
# Case 1 : Signature O / Extension O --> Carving
# Case 2 : Signature X / Extension O --> Print ("Not JPEG File (Signature Unmatch)")
# Case 3 : Signature O / Extension X --> Carving into JPEG File
# Case 4 : Signature X / Extension X

import tkinter
from tkinter import filedialog

import os

root = tkinter.Tk()
root.withdraw()

# dir_path 에 선택한 폴더 경로 저장
dir_path = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')

# count_list : Case 별 결과 수 기록
# jpeg_count : 전체 jpeg 계열 파일 수 기록
global count_list
global jpeg_count

count_list = [0, 0, 0, 0]
jpeg_count = 0


def JPEG_carving(file_path):
    global jpeg_count
    with open(file_path, 'rb') as f:
        buf = f.read()
        output = open('Carved_JPEG/' + str(jpeg_count) + '.jpeg', 'wb')
        output.write(buf)
        output.close()

    jpeg_count = jpeg_count + 1


# 선택한 폴더 대상 파일 카빙 시작
def search(dirname):
    global count_list

    try:
        # filenames : 해당 폴더 내의 파일/폴더
        filenames = os.listdir(dirname)

        # filename : 특정 파일/폴더의 경로
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)

            # 만약 폴더라면 재귀 검색
            if os.path.isdir(full_filename):
                search(full_filename)

            # 파일이라면
            else:
                with open(full_filename, 'rb') as f:

                    # ext : 파일 확장자
                    ext = os.path.splitext(full_filename)[-1]

                    # 확장자가 jpeg 형식 중 하나라면
                    if (ext == '.jpg') or (ext == '.jpeg') or (ext == '.jpe') or (ext == '.jfif'):

                        # buf_start : 헤더 시그니처, buf_end : 풋터 시그니처
                        buf_start = f.read(2)
                        f.seek(-2, 2)
                        buf_end = f.read(2)

                        # Case 1 (Signature O / Extension O)
                        if buf_start == b'\xff\xd8' and buf_end == b'\xff\xd9':
                            JPEG_carving(full_filename)
                            count_list[0] = count_list[0] + 1

                        # Case 2 (Signature X / Extension O)
                        else:
                            count_list[1] = count_list[1] + 1

                    else:
                        buf_start = f.read(2)
                        f.seek(-2, 2)
                        buf_end = f.read(2)

                        # Case 3 (Signature O / Extension X)
                        if buf_start == b'\xff\xd8' and buf_end == b'\xff\xd9':
                            JPEG_carving(full_filename)
                            count_list[2] = count_list[2] + 1

                        # Case 4 (Signature X / Extension X)
                        else:
                            count_list[3] = count_list[3] + 1

                    f.close()

    # 폴더 열기 시 권한 오류 회피
    except PermissionError:
        pass


# 카빙한 파일 보관할 폴더 생성
if os.path.isdir('Carved_JPEG'):
    pass
else:
    os.mkdir('Carved_JPEG')

# Main
search(dir_path)

# 결과 출력
print('\n<JPEG Carving Result - {}>'.format(dir_path))
print('Case 1 - Sort of JPEG File (.jpg, .jpeg, .jfif, .spiff ...) : {}'.format(count_list[0]))
print('Case 2 - Fake JPEG File (Signature Not Match) : {}'.format(count_list[1]))
print('Case 3 - Wrong Extension, but actually JPEG File : {}'.format(count_list[2]))
print('Case 4 - Other Files : {}'.format(count_list[3]))

print('\nCarved Files are stored in "./Carved_JPEG" folder')