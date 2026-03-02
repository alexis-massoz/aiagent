from functions.get_files_info import get_files_info


print(f'Result for current directory:\n\t{get_files_info("calculator", ".")}')

print(f'Result for current directory:\n\t{get_files_info("calculator", "pkg")}')

print(f'Result for current directory:\n\t{get_files_info("calculator", "/bin")}')

print(f'Result for current directory:\n\t{get_files_info("calculator", "../")}')