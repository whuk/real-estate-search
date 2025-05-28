import os
import shutil
import subprocess

# 이전 빌드 파일 삭제
for folder in ['build', 'dist']:
    if os.path.exists(folder):
        shutil.rmtree(folder)

# 빌드 명령어 (간단한 버전)
cmd = [
    'pyinstaller',
    '--onefile',
    '--windowed',
    '--name=RealEstateSearch',
    'realEstate.py'
]

# favicon.ico가 있으면 추가
if os.path.exists('favicon.ico'):
    cmd.extend(['--icon=favicon.ico', '--add-data=favicon.ico;.'])

# 빌드 실행
subprocess.run(cmd)

# 빌드 후 파일 복사
if os.path.exists('favicon.ico') and os.path.exists('dist'):
    shutil.copy('favicon.ico', 'dist/favicon.ico')

print("\n빌드 완료! dist 폴더를 확인하세요.")