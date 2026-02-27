import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
import platform
import datetime

# 폰트 설정 (이전 작업 유지)
if platform.system() == "Windows":
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == "Darwin":
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# [레이아웃 설정]
st.set_page_config(page_title="NemoStore 매물 상세뷰", layout="wide")

# [데이터 선언]
item_data = {
    "isPriority": None,
    "articleType": 1,
    "id": "05bfdb5f-0471-45d4-b7fc-dd8edceae38a",
    "buildingManagementSerialNumber": "1117012900103000301011153",
    "agentId": None,
    "number": 926589,
    "previewPhotoUrl": "https://img.nemoapp.kr/article-photos/5abebd77-1306-4b77-8a65-25f24d68f15d/s.jpg",
    "smallPhotoUrls": [
        "https://img.nemoapp.kr/article-photos/5abebd77-1306-4b77-8a65-25f24d68f15d/s.jpg",
        "https://img.nemoapp.kr/article-photos/120f4e4b-17ca-486a-8427-b807865d55b1/s.jpg",
        "https://img.nemoapp.kr/article-photos/a7335353-fbad-4380-b606-3578c9b95435/s.jpg",
        "https://img.nemoapp.kr/article-photos/6f7f0fb1-a0b1-4ade-929a-7aa2479fb893/s.jpg",
        "https://img.nemoapp.kr/article-photos/65ab3303-d8e7-451b-a0ff-1e666b0f1051/s.jpg"
    ],
    "originPhotoUrls": [
        "https://img.nemoapp.kr/article-photos/5abebd77-1306-4b77-8a65-25f24d68f15d/l.jpg",
        "https://img.nemoapp.kr/article-photos/120f4e4b-17ca-486a-8427-b807865d55b1/l.jpg",
        "https://img.nemoapp.kr/article-photos/a7335353-fbad-4380-b606-3578c9b95435/l.jpg",
        "https://img.nemoapp.kr/article-photos/6f7f0fb1-a0b1-4ade-929a-7aa2479fb893/l.jpg",
        "https://img.nemoapp.kr/article-photos/65ab3303-d8e7-451b-a0ff-1e666b0f1051/l.jpg"
    ],
    "businessLargeCode": 11,
    "businessLargeCodeName": "휴게음식점",
    "businessMiddleCode": 1101,
    "businessMiddleCodeName": "커피점/카페",
    "priceType": 1,
    "priceTypeName": "임대",
    "deposit": 45000,
    "monthlyRent": 1700,
    "isPremiumClosed": False,
    "premium": 19000,
    "sale": 0,
    "maintenanceFee": 90,
    "floor": 1,
    "groundFloor": 3,
    "size": 16.53,
    "title": "[동부이촌동] 귀한 1층 대로변 매장 양도",
    "firstDeposit": 45000,
    "firstMonthlyRent": 1700,
    "firstPremium": 19000,
    "confirmedDateUtc": None,
    "nearSubwayStation": "이촌(국립중앙박물관)역, 도보 6분",
    "viewCount": 5,
    "favoriteCount": 0,
    "isInYourFavorited": None,
    "isMoveInDate": True,
    "moveInDate": None,
    "completionConfirmedDateUtc": None,
    "createdDateUtc": "2026-02-18T02:34:49.766811+00:00",
    "editedDateUtc": "2026-02-18T02:34:49.80787+00:00",
    "state": 1,
    "areaPrice": 377
}

# [데이터 포맷팅 함수]
def format_price(value):
    if value is None or value == 0:
        return "-"
    formatted_value = f"{int(value / 10):,}"
    return f"{formatted_value}만"

# [데이터 로드 - EDA용]
@st.cache_data
def load_all_data():
    db_path = r'data/nemo_store.db'
    if not os.path.exists(db_path):
        db_path = r'C:\ICB7\work\nemostore\data\nemo_store.db'
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM nemo_stores", conn)
        conn.close()
        # 가격 전처리 (만원 단위)
        price_cols = ['deposit', 'monthly_rent', 'premium', 'sale', 'maintenance_fee']
        for col in price_cols:
            if col in df.columns:
                df[col] = df[col] / 10
        return df
    return None

df_all = load_all_data()

# [1. Header 영역]
# ... (생략 또는 기존 코드 유지)
st.header(item_data['title'])
st.caption(f"📍 {item_data['businessMiddleCodeName']} | 지상 {item_data['floor']}층 (총 {item_data['groundFloor']}층 빌딩) | 전용 {item_data['size']}㎡")

# 태그 표시
created_date = datetime.datetime.fromisoformat(item_data['createdDateUtc'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
st.markdown(f"""
<div style="display: flex; gap: 10px; margin-bottom: 20px;">
    <span style="background-color: #f0f2f6; padding: 5px 12px; border-radius: 15px; font-size: 0.85rem; color: #555;">🚇 {item_data['nearSubwayStation']}</span>
    <span style="background-color: #f0f2f6; padding: 5px 12px; border-radius: 15px; font-size: 0.85rem; color: #555;">📅 등록일: {created_date}</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# [2. 매물 이미지 영역]
st.subheader("📸 매물 이미지")
img_cols = st.columns(len(item_data['originPhotoUrls']))
for idx, img_url in enumerate(item_data['originPhotoUrls']):
    with img_cols[idx]:
        st.image(img_url, use_container_width=True)

st.divider()

# [3. 핵심 임대 정보 뷰어]
st.subheader("💰 임대 및 주요 정보")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="보증금", value=format_price(item_data['deposit']))
with m_col2:
    st.metric(label="월세", value=format_price(item_data['monthlyRent']), delta="부가세 별도", delta_color="off")
with m_col3:
    st.metric(label="권리금", value=format_price(item_data['premium']))
with m_col4:
    st.metric(label="월 관리비", value=format_price(item_data['maintenanceFee']))

st.divider()

# [4. 상세 정보 탭]
tab1, tab2, tab3, tab4 = st.tabs(["📑 매물 상세 특징", "🏢 건축물 대장 정보", "🗺️ 위치 정보", "📊 시장 분석 (EDA)"])

with tab1:
    st.markdown("""
    ### 중개사 코멘트
    - **동부이촌동에서 귀하다는 1층 대로변 상가**
    - 신용산초 / 용강중 / 중경고 인접, 아파트 단지 밀집되어 유동인구 풍부
    - 항아리 상권 특성상 고정 수요 기반이 탄탄하고 매출 변동성이 낮음
    - 한강공원 인접으로 평일/주말 가리지 않는 외부 유입 수요 확보
    - **현재 요거트 전문점 운영 중**이며, 인테리어 및 시설 매우 깔끔함
    
    [권리금 상세]
    - 요커 그대로 인수 시: **2,500만원** (각종 설비, 레시피 일체 포함)
    - 매장 단독 인수 시: **1,900만원** (무인샵, 카페, 네일샵 등 다양한 업종 협의 가능)
    """)

with tab2:
    build_info = {
        "항목": ["건축물 용도", "사용승인일", "주구조", "층수", "연면적", "주차 가능 여부", "엘리베이터"],
        "내용": ["제1종 근린생활시설", "1979.12.17", "철근콘크리트구조", "지하 1층 ~ 지상 3층", "2,417.98㎡", "1대 (자주식)", "없음"]
    }
    st.table(pd.DataFrame(build_info))

with tab3:
    st.markdown(f"""
    ### 주변 환경 및 상권 분석
    - **지하철**: {item_data['nearSubwayStation']}로 대중교통 접근성 우수함.
    - **주변 시설**: 신용산초등학교(도보 1분), 이촌역(도보 7분), 국립중앙박물관 인접.
    - **상권 특징**: 전형적인 주거 배후 상권으로 안정적인 매출 발생 가능 지역.
    - **추천 업종**: 소규모 카페, 배달 전문점, 1인 뷰티샵, 테이크아웃 전문점 등.
    """)

with tab4:
    if df_all is not None:
        st.subheader("🛒 시장 데이터 탐색 (EDA)")
        
        # [EDA 전용 필터]
        with st.expander("🔍 데이터 필터링 옵션", expanded=True):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                all_types = ["전체"] + sorted(df_all['business_middle_code_name'].unique().tolist())
                selected_type = st.selectbox("업종 선택", all_types, key="eda_type_filter")
            with f_col2:
                all_floors = ["전체"] + sorted(df_all['floor'].unique().tolist())
                selected_floor = st.selectbox("층수 선택", all_floors, key="eda_floor_filter")
            with f_col3:
                min_s, max_s = float(df_all['size'].min()), float(df_all['size'].max())
                eda_size_range = st.slider("면적 범위 (㎡)", min_s, max_s, (min_s, max_s), key="eda_size_slider")
        
        # 데이터 필터링 적용
        df_eda = df_all.copy()
        if selected_type != "전체":
            df_eda = df_eda[df_eda['business_middle_code_name'] == selected_type]
        if selected_floor != "전체":
            df_eda = df_eda[df_eda['floor'] == selected_floor]
        df_eda = df_eda[(df_eda['size'] >= eda_size_range[0]) & (df_eda['size'] <= eda_size_range[1])]

        # 0. KPI 섹션 (필터링된 데이터 반영)
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        k_col1.metric("필터링된 매물", f"{len(df_eda)}건")
        if len(df_eda) > 0:
            k_col2.metric("평균 보증금", f"{df_eda['deposit'].mean():,.0f}만")
            k_col3.metric("평균 월세", f"{df_eda['monthly_rent'].mean():,.0f}만")
            k_col4.metric("평균 면적", f"{df_eda['size'].mean():.1f}㎡")
        else:
            k_col2.metric("평균 보증금", "-")
            k_col3.metric("평균 월세", "-")
            k_col4.metric("평균 면적", "-")
        
        st.divider()
        
        if len(df_eda) > 0:
            # 1. 가격 분포 분석
            st.markdown("#### 🔘 주요 가격대 분포")
            c1, c2, c3 = st.columns(3)
            with c1:
                fig, ax = plt.subplots()
                ax.hist(df_eda['deposit'], bins=10, color='skyblue', edgecolor='black')
                ax.set_title("보증금 분포 (만원)")
                st.pyplot(fig)
            with c2:
                fig, ax = plt.subplots()
                ax.hist(df_eda['monthly_rent'], bins=10, color='salmon', edgecolor='black')
                ax.set_title("월세 분포 (만원)")
                st.pyplot(fig)
            with c3:
                fig, ax = plt.subplots()
                ax.hist(df_eda['premium'], bins=10, color='lightgreen', edgecolor='black')
                ax.set_title("권리금 분포 (만원)")
                st.pyplot(fig)
                
            st.divider()
            
            # 2. 업종 및 면적 분석
            v1, v2 = st.columns(2)
            with v1:
                st.markdown("#### 🏷️ 업종별 매물 현황")
                type_counts = df_eda['business_middle_code_name'].value_counts()
                fig, ax = plt.subplots()
                if not type_counts.empty:
                    type_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, cmap='Pastel1')
                ax.set_ylabel("")
                st.pyplot(fig)
            with v2:
                st.markdown("#### 📏 면적 대비 월세 상관관계")
                fig, ax = plt.subplots()
                ax.scatter(df_eda['size'], df_eda['monthly_rent'], color='purple', alpha=0.6)
                ax.set_xlabel("전용면적 (㎡)")
                ax.set_ylabel("월세 (만원)")
                ax.set_title("면적 vs 월세")
                st.pyplot(fig)
        else:
            st.warning("선택한 필터 조건에 맞는 매물이 없습니다.")
            
        st.divider()
        
        # KPI로 대체됨 (시장 통계 요약 삭제)
        st.caption("※ 위 통계는 데이터베이스에 등록된 전체 매물을 기준으로 산출되었습니다.")
    else:
        st.warning("데이터베이스 파일을 찾을 수 없어 시장 분석 데이터를 로드할 수 없습니다.")


# Footer
st.sidebar.markdown("### 📊 NemoStore Insight")
st.sidebar.write("해당 매물은 동부이촌동 핵심 상권에 위치해 있습니다.")
st.sidebar.progress(85, text="상권 활성도")
st.sidebar.divider()
st.sidebar.caption("© 2026 NemoStore Dashboard. All rights reserved.")
