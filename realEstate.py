
import sys
import json
import requests
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLineEdit, QLabel,
                             QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
                             QTabWidget, QGroupBox, QRadioButton, QSpinBox,
                             QSplitter, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QSize, Signal, Slot
from PySide6.QtGui import QIcon
from datetime import datetime
import os

# PyInstaller 호환성을 위한 pandas import
try:
    import pandas as pd
    import openpyxl
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class NaverRealEstateAPI:
    def __init__(self):
        self.cookies = {
            'NNB': 'H72JBUL7UWSWM',
            'NSCS': '2',
            'ASID': 'daec443200000191558b90550000004d',
            'ba.uuid': '5384a23d-95d1-428a-92be-4619cb1512a8',
            'BNB_FINANCE_HOME_TOOLTIP_MYASSET': 'true',
            'NAC': 'CArzBggxTz95',
            '_ga': 'GA1.1.186245813.1725276141',
            '_fbp': 'fb.1.1743593010106.557674768149567682',
            '_ga_TC04LC8Q7L': 'GS1.1.1743595852.2.0.1743595852.60.0.0',
            'NID_AUT': '8gNWs077cSACbUi0GGex1kmPAwm9UhPUjoQr88denDNQY7UPnZ2x/iO4uh6WZsJM',
            'NID_JKL': '5KYk1fJ/ixz9j6Hv9XBAx4J+If9z/QqR1b+Sj3QgV+U=',
            '_fwb': '133O9BaXDFP4BWG9HhDBvZE.1745321776322',
            'landHomeFlashUseYn': 'Y',
            'nhn.realestate.article.rlet_type_cd': 'A01',
            'nhn.realestate.article.trade_type_cd': '""',
            'realestate.beta.lastclick.cortar': '1138000000',
            'NACT': '1',
            'SRT30': '1747652250',
            'SRT5': '1747652250',
            'NID_SES': 'AAABq6k8CqfDdNPeyq1xnoW4fHxDsVqbMVK5tOEjnz+uZrZjBYWfOXqJmxtiXRzXibjBgx7pOZ80Nda9Z6WkAuG+d/QZwLhZ69VaxscEdl7EezMGLIBkxMifN/snooUN8+d5JYyJ8APRxY4FNOCF/uk05aj+tJnjXL/K1lQVlaMk/3MlmO0bqmJdPGEAzqPCG6lPaD05/QHN45H8i3VZ979xoXVSphpeEfoaAemvXfEZ7cvtWLT6ebQz8iCsi/YJmWHLvCXObkQIVee4m2UF3Rs1jMRbRyRxCi7ATO9GhQVYirg4eCjz0R/9XV7XX6D9SnCqq3hdiH9I3ORKb9j21j2G8VsEmQr7VOVbtqX+e8KtqRRsEIhpljxG2pJEpSWLKMt+Zjk+7yK0yH+7LEgyMAUAxkFucTROqK8fcTq5QmuyllJqY6ijz9A/azZlNSyVy6TtX2DbrD76OCJ4/j6IzD0icRDEW4lwN5FxPZoqhNCK006bV+SsgFdPIlxEgEVlW4GyK9foZB3N673ytp6F7GE/J5TWa6SubLcvg0+Vn8/1JaeejGgomooh5x/MjxfOMrZalQ==',
            '_naver_usersession_': 'GGjDC1nG/89oZS7nGPtGov9G',
            'page_uid': 'juVMrsqVN8CssBGr3p8ssssssFZ-505663',
            'REALESTATE': 'Mon%20May%2019%202025%2019%3A57%3A49%20GMT%2B0900%20(Korean%20Standard%20Time)',
            'BUC': '09yku-QzF8GQ5s7TrWgc3oIVbfuKDEvvDQUySMnfAfA=',
        }

        self.headers = {
            'accept': '*/*',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NDc2NTIyNjksImV4cCI6MTc0NzY2MzA2OX0.7z-0Bu1lyhdtER1V2aPojELmySJu8ssmg1Ha1lr8qrE',
            'priority': 'u=1, i',
            'referer': 'https://new.land.naver.com/complexes/107610?ms=37.606856,126.936368,17&a=APT:ABYG:JGC:PRE&e=RETAIL',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        }
    
    def search_keyword(self, keyword):
        """키워드로 아파트 검색"""
        params = {'keyword': keyword}
        response = requests.get('https://new.land.naver.com/api/search', 
                               params=params, cookies=self.cookies, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return {"complexes": [], "regions": [], "isMoreData": False}

    def get_articles(self, complex_no, trade_type="", price_min=0, price_max=900000000):
        """아파트 매물 검색"""
        all_articles = []
        page = 1
        
        # 거래 유형에 따른 URL 설정
        trade_type_param = ""
        if trade_type:
            trade_type_param = f"&tradeType={trade_type}"
        
        while True:
            url = f'https://new.land.naver.com/api/articles/complex/{complex_no}?realEstateType=APT%3AABYG%3AJGC%3APRE{trade_type_param}&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin={price_min}&priceMax={price_max}&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo={complex_no}&buildingNos=&areaNos=&type=list&order=rank'
            
            response = requests.get(url, cookies=self.cookies, headers=self.headers)
            
            if response.status_code != 200:
                break
                
            data = response.json()
            
            if not data.get('articleList'):
                break
                
            all_articles.extend(data['articleList'])
            
            if not data.get('isMoreData'):
                break
                
            page += 1
            
        return all_articles
    
    def group_articles_by_building_floor(self, articles):
        """동, 호수 기준으로 매물 그룹화"""
        grouped_articles = {}

        for article in articles:
            # 동 정보와 호수 정보를 추출 (buildingName은 동 정보를 포함)
            building_name = article.get('buildingName', '')
            floor_info = article.get('floorInfo', '')
            
            # 매물의 고유 식별키 생성 - 동일한 건물(동)과 층수를 가진 매물을 묶기 위함
            property_key = f"{building_name}_{floor_info}"
            
            # 부동산 정보를 담을 객체 생성
            realtor_info = {
                'realtorName': article.get('realtorName', ''),
                'realtorId': article.get('realtorId', ''),
                'cpName': article.get('cpName', ''),
                'cpid': article.get('cpid', ''),
                'articleNo': article.get('articleNo', ''),
                'articleFeatureDesc': article.get('articleFeatureDesc', ''),
                'articleConfirmYmd': article.get('articleConfirmYmd', ''),  # 등록일
                'articleListUpdateYmd': article.get('articleListUpdateYmd', '')  # 수정일
            }
            
            # 같은 동, 층에 대한 매물이 이미 있으면 부동산 정보만 추가
            if property_key in grouped_articles:
                grouped_articles[property_key]['realtors'].append(realtor_info)
                # 가장 최근 날짜로 업데이트
                if article.get('articleConfirmYmd', '') > grouped_articles[property_key].get('articleConfirmYmd', ''):
                    grouped_articles[property_key]['articleConfirmYmd'] = article.get('articleConfirmYmd', '')
                if article.get('articleListUpdateYmd', '') > grouped_articles[property_key].get('articleListUpdateYmd', ''):
                    grouped_articles[property_key]['articleListUpdateYmd'] = article.get('articleListUpdateYmd', '')
            else:
                # 새로운 매물 정보 생성. 공통 정보는 그대로 유지하고 부동산 관련 정보만 배열로 관리
                grouped_article = {key: value for key, value in article.items() if key not in ['realtorName', 'realtorId', 'cpName', 'cpid', 'articleNo', 'articleFeatureDesc', 'articleConfirmYmd', 'articleListUpdateYmd']}
                grouped_article['realtors'] = [realtor_info]
                # 날짜 정보는 공통 정보로 추가
                grouped_article['articleConfirmYmd'] = article.get('articleConfirmYmd', '')
                grouped_article['articleListUpdateYmd'] = article.get('articleListUpdateYmd', '')
                grouped_articles[property_key] = grouped_article

        # 그룹화된 매물 목록 반환
        return list(grouped_articles.values())

class PropertySearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = NaverRealEstateAPI()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('네이버 부동산 매물 검색기')
        self.setGeometry(100, 100, 1000, 800)  # 가로 길이를 1200에서 1000으로 줄임
        
        # 파비콘 설정
        icon_path = os.path.join(os.path.dirname(__file__), 'favicon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 메인 위젯 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # 검색 영역
        search_group = QGroupBox('아파트 검색')
        search_layout = QVBoxLayout(search_group)
        
        # 키워드 검색
        keyword_layout = QHBoxLayout()
        keyword_layout.addWidget(QLabel('키워드:'))
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText('지역명 또는 아파트명 입력 (예: 녹번동 북한산푸르지오)')
        self.keyword_input.returnPressed.connect(self.search_keyword)
        keyword_layout.addWidget(self.keyword_input)
        
        self.search_btn = QPushButton('검색')
        self.search_btn.clicked.connect(self.search_keyword)
        keyword_layout.addWidget(self.search_btn)
        search_layout.addLayout(keyword_layout)
        
        # 검색 결과 테이블
        self.search_result_table = QTableWidget()
        self.search_result_table.setColumnCount(4)
        self.search_result_table.setHorizontalHeaderLabels(['아파트명', '지역', '타입', '세대수'])
        # 칼럼별 리사이즈 모드 설정
        header = self.search_result_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 아파트명 - Stretch
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # 지역 - Stretch
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 타입 - 내용에 맞춤
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 세대수 - 내용에 맞춤
        self.search_result_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.search_result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.search_result_table.itemDoubleClicked.connect(self.select_complex)
        self.search_result_table.setMinimumHeight(150)  # 최소 높이를 150으로 줄임
        self.search_result_table.setMaximumHeight(200)  # 최대 높이 설정으로 5개 row 정도만 표시
        search_layout.addWidget(self.search_result_table)
        
        # 필터 영역
        filter_group = QGroupBox('매물 필터')
        filter_layout = QHBoxLayout(filter_group)
        
        # 거래 유형 필터
        trade_type_group = QGroupBox('거래 유형')
        trade_type_layout = QVBoxLayout(trade_type_group)
        
        self.trade_type_all = QRadioButton('전체')
        self.trade_type_all.setChecked(True)
        self.trade_type_sale = QRadioButton('매매')
        self.trade_type_jeonse = QRadioButton('전세')
        self.trade_type_monthly = QRadioButton('월세')
        
        trade_type_layout.addWidget(self.trade_type_all)
        trade_type_layout.addWidget(self.trade_type_sale)
        trade_type_layout.addWidget(self.trade_type_jeonse)
        trade_type_layout.addWidget(self.trade_type_monthly)
        filter_layout.addWidget(trade_type_group)
        
        # 가격 필터
        price_group = QGroupBox('가격 범위 (만원)')
        price_layout = QVBoxLayout(price_group)
        
        price_min_layout = QHBoxLayout()
        price_min_layout.addWidget(QLabel('최소 가격:'))
        self.price_min_input = QSpinBox()
        self.price_min_input.setRange(0, 1000000)
        self.price_min_input.setSingleStep(1000)
        price_min_layout.addWidget(self.price_min_input)
        price_layout.addLayout(price_min_layout)
        
        price_max_layout = QHBoxLayout()
        price_max_layout.addWidget(QLabel('최대 가격:'))
        self.price_max_input = QSpinBox()
        self.price_max_input.setRange(0, 1000000)
        self.price_max_input.setSingleStep(1000)
        self.price_max_input.setValue(90000)
        price_max_layout.addWidget(self.price_max_input)
        price_layout.addLayout(price_max_layout)
        
        filter_layout.addWidget(price_group)
        
        # 버튼 레이아웃
        button_layout = QVBoxLayout()
        
        # 검색 버튼
        self.search_articles_btn = QPushButton('매물 검색')
        self.search_articles_btn.setEnabled(False)
        self.search_articles_btn.clicked.connect(self.search_articles)
        button_layout.addWidget(self.search_articles_btn)
        
        # csv 다운로드 버튼
        self.download_excel_btn = QPushButton('엑셀 다운로드')
        self.download_excel_btn.setEnabled(False)
        self.download_excel_btn.clicked.connect(self.download_excel)
        button_layout.addWidget(self.download_excel_btn)
        
        filter_layout.addLayout(button_layout)
        
        # 매물 결과 테이블
        article_group = QGroupBox('매물 목록')
        article_layout = QVBoxLayout(article_group)
        
        self.article_table = QTableWidget()
        self.article_table.setColumnCount(8)
        self.article_table.setHorizontalHeaderLabels(['동', '층', '평형', '가격', '방향', '등록일', '중개사 수', '설명'])
        
        # 칼럼별 리사이즈 모드 설정
        header = self.article_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 동 - 내용에 맞춤
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 층 - 내용에 맞춤
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 평형 - 내용에 맞춤
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 가격 - 내용에 맞춤
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 방향 - 내용에 맞춤
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # 등록일 - 내용에 맞춤
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # 중개사 수 - 내용에 맞춤
        header.setSectionResizeMode(7, QHeaderView.Stretch)  # 설명 - Stretch (남은 공간 채우기)
        
        # 칼럼 초기 너비 설정
        self.article_table.setColumnWidth(0, 80)   # 동
        self.article_table.setColumnWidth(1, 60)   # 층
        self.article_table.setColumnWidth(2, 120)  # 평형
        self.article_table.setColumnWidth(3, 100)  # 가격
        self.article_table.setColumnWidth(4, 60)   # 방향
        self.article_table.setColumnWidth(5, 100)  # 등록일
        self.article_table.setColumnWidth(6, 80)   # 중개사 수
        
        self.article_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.article_table.itemDoubleClicked.connect(self.show_realtor_details)
        article_layout.addWidget(self.article_table)
        
        # 상태 표시 영역
        status_layout = QHBoxLayout()
        self.status_label = QLabel('준비됨')
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()  # 중간 공간 추가
        
        # made by 문구 추가
        made_by_label = QLabel('made by lala-friends')
        made_by_label.setStyleSheet('color: #666666; font-size: 11px; font-style: italic;')
        status_layout.addWidget(made_by_label)
        
        # 레이아웃 배치
        splitter = QSplitter(Qt.Vertical)
        search_widget = QWidget()
        search_widget.setLayout(QVBoxLayout())
        search_widget.layout().addWidget(search_group)
        search_widget.layout().addWidget(filter_group)
        
        article_widget = QWidget()
        article_widget.setLayout(QVBoxLayout())
        article_widget.layout().addWidget(article_group)
        
        splitter.addWidget(search_widget)
        splitter.addWidget(article_widget)
        splitter.setSizes([350, 450])  # 검색 영역 크기 조정
        
        main_layout.addWidget(splitter)
        main_layout.addLayout(status_layout)
        
        # 변수 초기화
        self.selected_complex = None
        self.current_articles = []  # 현재 표시된 매물 데이터 저장
        
    def search_keyword(self):
        keyword = self.keyword_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, '입력 오류', '검색어를 입력해주세요.')
            return
            
        self.status_label.setText(f"'{keyword}' 검색 중...")
        QApplication.processEvents()
        
        try:
            result = self.api.search_keyword(keyword)
            
            self.search_result_table.setRowCount(0)
            if 'complexes' in result and result['complexes']:
                complexes = result['complexes']
                self.search_result_table.setRowCount(len(complexes))
                
                for row, complex_data in enumerate(complexes):
                    self.search_result_table.setItem(row, 0, QTableWidgetItem(complex_data.get('complexName', '')))
                    self.search_result_table.setItem(row, 1, QTableWidgetItem(complex_data.get('cortarAddress', '')))
                    self.search_result_table.setItem(row, 2, QTableWidgetItem(complex_data.get('realEstateTypeName', '')))
                    self.search_result_table.setItem(row, 3, QTableWidgetItem(str(complex_data.get('totalHouseholdCount', 0))))
                    
                    # 테이블 항목에 데이터 저장
                    for col in range(4):
                        item = self.search_result_table.item(row, col)
                        if item:
                            item.setData(Qt.UserRole, complex_data)
                
                self.status_label.setText(f"'{keyword}' 검색 완료. {len(complexes)}개의 결과를 찾았습니다.")
            else:
                self.status_label.setText(f"'{keyword}' 검색 결과가 없습니다.")
        except Exception as e:
            self.status_label.setText(f"검색 중 오류 발생: {str(e)}")
            QMessageBox.critical(self, '오류', f"검색 중 오류가 발생했습니다: {str(e)}")
    
    def select_complex(self, item):
        self.selected_complex = item.data(Qt.UserRole)
        if self.selected_complex:
            complex_name = self.selected_complex.get('complexName', '')
            self.search_articles_btn.setEnabled(True)
            self.status_label.setText(f"'{complex_name}' 아파트가 선택되었습니다. 매물 검색을 시작하세요.")
    
    def get_trade_type(self):
        if self.trade_type_all.isChecked():
            return ""
        elif self.trade_type_sale.isChecked():
            return "A1"  # 매매
        elif self.trade_type_jeonse.isChecked():
            return "B1"  # 전세
        elif self.trade_type_monthly.isChecked():
            return "B2"  # 월세
        return ""
    
    def format_date(self, date_str):
        """날짜 형식 변환 (YYYYMMDD -> YYYY-MM-DD)"""
        if not date_str or len(date_str) != 8:
            return ''
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            return date_obj.strftime('%Y-%m-%d')
        except:
            return date_str
    
    def search_articles(self):
        if not self.selected_complex:
            QMessageBox.warning(self, '선택 오류', '아파트를 먼저 선택해주세요.')
            return
        
        complex_no = self.selected_complex.get('complexNo')
        complex_name = self.selected_complex.get('complexName', '')
        
        # 필터 값 가져오기
        trade_type = self.get_trade_type()
        price_min = self.price_min_input.value() * 10000  # 만원 단위를 원 단위로 변환
        price_max = self.price_max_input.value() * 10000
        
        self.status_label.setText(f"'{complex_name}' 매물 검색 중...")
        QApplication.processEvents()
        
        try:
            # 매물 검색
            articles = self.api.get_articles(complex_no, trade_type, price_min, price_max)
            
            if not articles:
                self.status_label.setText(f"'{complex_name}' 매물이 없습니다.")
                self.article_table.setRowCount(0)
                return
            
            # 매물 그룹화
            grouped_articles = self.api.group_articles_by_building_floor(articles)
            
            # 등록일 기준으로 최신순 정렬
            grouped_articles.sort(key=lambda x: x.get('articleConfirmYmd', ''), reverse=True)
            
            # 현재 매물 데이터 저장
            self.current_articles = grouped_articles
            
            # 결과 테이블에 표시
            self.article_table.setRowCount(0)
            self.article_table.setRowCount(len(grouped_articles))
            
            for row, article in enumerate(grouped_articles):
                self.article_table.setItem(row, 0, QTableWidgetItem(article.get('buildingName', '')))
                self.article_table.setItem(row, 1, QTableWidgetItem(article.get('floorInfo', '')))
                self.article_table.setItem(row, 2, QTableWidgetItem(f"{article.get('areaName', '')} ({article.get('area1', '')}/{article.get('area2', '')}㎡)"))
                self.article_table.setItem(row, 3, QTableWidgetItem(article.get('dealOrWarrantPrc', '')))
                self.article_table.setItem(row, 4, QTableWidgetItem(article.get('direction', '')))
                
                # 날짜 정보 표시
                confirm_date = self.format_date(article.get('articleConfirmYmd', ''))
                self.article_table.setItem(row, 5, QTableWidgetItem(confirm_date))
                
                realtors = article.get('realtors', [])
                realtors_count = len(realtors)
                self.article_table.setItem(row, 6, QTableWidgetItem(str(realtors_count)))
                
                # 특징 설명
                if realtors:
                    self.article_table.setItem(row, 7, QTableWidgetItem(realtors[0].get('articleFeatureDesc', '')))
                
                # 테이블 항목에 데이터 저장
                for col in range(8):
                    item = self.article_table.item(row, col)
                    if item:
                        item.setData(Qt.UserRole, article)
            
            self.status_label.setText(f"'{complex_name}' 매물 검색 완료. 총 {len(articles)}개의 매물, {len(grouped_articles)}개의 그룹으로 표시됨.")
            
            # 엑셀 다운로드 버튼 활성화
            self.download_excel_btn.setEnabled(True)
        except Exception as e:
            self.status_label.setText(f"매물 검색 중 오류 발생: {str(e)}")
            QMessageBox.critical(self, '오류', f"매물 검색 중 오류가 발생했습니다: {str(e)}")
    
    def show_realtor_details(self, item):
        article = item.data(Qt.UserRole)
        if not article:
            return
        
        realtors = article.get('realtors', [])
        if not realtors:
            return
        
        dialog = QMessageBox(self)
        dialog.setWindowTitle('중개사무소 정보')
        
        building_name = article.get('buildingName', '')
        floor_info = article.get('floorInfo', '')
        area_name = article.get('areaName', '')
        price = article.get('dealOrWarrantPrc', '')
        
        message = f"<b>{building_name} {floor_info} ({area_name}) - {price}</b><br><br>"
        message += f"<b>총 {len(realtors)}개의 중개사무소:</b><br><br>"
        
        for i, realtor in enumerate(realtors, 1):
            confirm_date = self.format_date(realtor.get('articleConfirmYmd', ''))
            update_date = self.format_date(realtor.get('articleListUpdateYmd', ''))
            
            message += f"<b>{i}. {realtor.get('realtorName', '')}</b> (매물번호: {realtor.get('articleNo', '')})<br>"
            message += f"- 등록일: {confirm_date}, 수정일: {update_date}<br>"
            message += f"- {realtor.get('articleFeatureDesc', '')}<br><br>"
        
        dialog.setText(message)
        dialog.setTextFormat(Qt.RichText)
        dialog.exec()

    def download_excel(self):
        """매물 검색 결과를 엑셀로 다운로드 (간단한 방식)"""
        if not self.current_articles:
            QMessageBox.warning(self, '다운로드 오류', '다운로드할 매물 데이터가 없습니다.')
            return

        # 파일 저장 대화상자 - CSV로 저장하되 엑셀에서 열 수 있음
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '파일 저장',
            f'{self.selected_complex.get("complexName", "매물목록")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            'CSV Files (*.csv);;All Files (*.*)'
        )

        if not file_path:
            return

        try:
            # CSV 파일로 저장 (엑셀에서 바로 열림)
            import csv

            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['동', '층', '평형', '전용면적(㎡)', '공급면적(㎡)', '가격', '방향',
                              '등록일', '중개사무소 수', '중개사무소', '매물번호', '특징설명']

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for article in self.current_articles:
                    realtors = article.get('realtors', [])

                    base_info = {
                        '동': article.get('buildingName', ''),
                        '층': article.get('floorInfo', ''),
                        '평형': article.get('areaName', ''),
                        '전용면적(㎡)': article.get('area1', ''),
                        '공급면적(㎡)': article.get('area2', ''),
                        '가격': article.get('dealOrWarrantPrc', ''),
                        '방향': article.get('direction', ''),
                        '등록일': self.format_date(article.get('articleConfirmYmd', '')),
                        '중개사무소 수': len(realtors)
                    }

                    if realtors:
                        for realtor in realtors:
                            row = base_info.copy()
                            row['중개사무소'] = realtor.get('realtorName', '')
                            row['매물번호'] = realtor.get('articleNo', '')
                            row['특징설명'] = realtor.get('articleFeatureDesc', '')
                            writer.writerow(row)
                    else:
                        writer.writerow(base_info)

            self.status_label.setText(f"파일이 저장되었습니다: {os.path.basename(file_path)}")
            QMessageBox.information(self, '저장 완료', '파일이 성공적으로 저장되었습니다.\n엑셀에서 열어보실 수 있습니다.')

        except Exception as e:
            self.status_label.setText(f"파일 저장 중 오류 발생: {str(e)}")
            QMessageBox.critical(self, '저장 오류', f"파일 저장 중 오류가 발생했습니다:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PropertySearchApp()
    window.show()
    sys.exit(app.exec())