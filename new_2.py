# Usage: streamlit run AIp05數據框轉換X.py --> http:/localhost:8501

import numpy as np
import pandas as pd
from st_aggrid import AgGrid #, GridUpdateMode, JsCode, ColumnsAutoSizeMode
import plotly.express as px
import plotly.graph_objs as go

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from datetime import date, datetime

#%%####### (W).網站系統基本架構 ##########
import streamlit as st
from streamlit_navigation_bar import st_navbar

# 建筑年龄（百年老房、50年以上、20-50年、小于20年） 不同地区、每平均价、交易量、用户画像（商/居）
# 建筑材料（混凝土、木材、石材、其他） 每平均价、交易量、用户画像（商/居）
# 季度（四季度） 每平均价、交易量

#%%##===== (D4) 系統基本架構 [*網站.py(E4)] =====#####


#%%##===== (W1).自定公用函式庫 =====#####
# @st.cache_data
def getX(Xname):     ##== X = getX(Xname): 自 X.csv 讀取 X (KDD1), 並設定標籤 (KDD3) ==##
    XXX = pd.read_csv(Xname)
    XXX["date"] = pd.to_datetime(XXX["datetime"]).dt.date
    XXX["year"] = pd.to_datetime(XXX["datetime"]).dt.year
    XXX["month"] = pd.to_datetime(XXX["datetime"]).dt.month
    XXX["yq"] = pd.PeriodIndex(XXX.date, freq='Q')
    # XXX["ym"] = pd.PeriodIndex(XXX.date, freq='M')

    XXX["quarter"] = pd.cut(XXX["month"], bins=[0, 3, 6, 9, 12], labels=["1", "2", "3", "4"])  #把月份离散处理成季度
    XXX["AR"] = pd.cut(XXX["age"],bins=[0,10,20,30,50,100]).astype(str) #屋齡离散化 AgeRange

    return (XXX)

def sumX(df,ages,length,usefor):
    scores=[]
    
    scores.append({"屋齡":ages[0],usefor[0]:length[0][0], usefor[1]:length[0][1],usefor[2]:length[0][2],usefor[3]:length[0][3],usefor[4]:length[0][4]})
    scores.append({"屋齡":ages[1],usefor[0]:length[1][0], usefor[1]:length[1][1],usefor[2]:length[1][2],usefor[3]:length[1][3],usefor[4]:length[1][4]})
    scores.append({"屋齡":ages[2],usefor[0]:length[2][0], usefor[1]:length[2][1],usefor[2]:length[2][2],usefor[3]:length[2][3],usefor[4]:length[2][4]})
    scores.append({"屋齡":ages[3],usefor[0]:length[3][0], usefor[1]:length[3][1],usefor[2]:length[3][2],usefor[3]:length[3][3],usefor[4]:length[3][4]})
    #scores.append({"屋齡":ages[4],usefor[0]:length[l][0], usefor[1]:length[l][1],usefor[2]:length[l][2],usefor[3]:length[l][3]})

    score_df = pd.DataFrame(scores)

    return score_df

#%%##===== (W2).儀表板函式庫: 前台(a)navbar,(b)sidebar,(c)canvas,後台(d) =====#####
def 擷取交易(fname):  ##== (KDD1)擷取交易儀表板: X = 擷取交易(fnameX) ==##
    ##== (d).後台 ==##
    X = getX(fname)
    print("\n\n>>>>> 擷取交易數據 (-->XXX) -----")  # -- 偵錯用

    data = {
        "columns": [
            "地段","datetime","total_price","unit_price","area","主建物佔比","型態",
            "age","樓別/樓高","交易標的","交易筆棟數","建物現況格局","parking_price","管理組織",
            "電梯","主要用途","備註"
        ],
        "說明": [
            "信義區的路段","交易日期","總價（以台幣為單位）", "單位價格", "坪數","實際可使用坪數","房子型態",
            "屋齡","樓別/樓高","實際獲得","--","--","車位價格","有無管理單位",
            "有無電梯","住家or商等","--"
        ]
    }
    df = pd.DataFrame(data)
    # 选择特定的列
    selected_columns = X[['year', 'month', 'yq',  'quarter', 'AR']]
    # 设置显示 index
    selected_columns_with_index = selected_columns.set_index(X.index)

    # 热力图
    corr_matrix = X.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)

    # == (b).前台-sidebar ==##  #==> [[AIp04/C4)(2)垂直流程]]
    st.markdown("---")
    st.sidebar.header("== (KDD1) 擷取交易數據 -- ")
    st.sidebar.write("* 交易檔名 = " + fname)
    st.sidebar.write("* 記錄筆數 = ", X.shape[0])
    ##== (c).前台-canvas ==##


    title = '<h2 style="font-family:sans-serif;text-align:center">(KDD1) 擷取交易數據 %s</h2>'%(fname)
    st.markdown(title, unsafe_allow_html=True)
    st.subheader("1-1. 原始數據展示")
    st.write("* 數據來源：https://plvr.land.moi.gov.tw/DownloadOpenData")
    st.write("* 記錄筆數 = " + str(X.shape[0]))
    st.dataframe(X.head(5))
    # ==> [[AIp04/C4)(1)水平流程]]
    st.subheader("1-2. 數據說明")
    
    cols1 = st.columns([1,1])
    cols1[0].table(df)
    st.markdown("---")

    
    st.html("<h2  style='text-align:center;margin:0 0 3% 0'>== (KDD2) 探索交易數據--</h2>")

    cols = st.columns([1, 1])  # -- (d).前台--canvas
    correlation_map = '<h3 style="text-align:center;font-family:sans-serif;">* Correlation</h3>'
    cols[0].markdown(correlation_map, unsafe_allow_html=True)
    cols[0].pyplot(plt)
    a = '<h3  style="text-align:center;font-family:sans-serif;">2.說明</h3>'
    cols[1].markdown(a, unsafe_allow_html=True)
    cols[1].html("""<p style='text-align: left;'>1. <span style="background-color:yellow">total_price & area：相關係數接近 0.94</span>，表現出<span style="background-color:yellow">強烈的正相關</span>。
                                                <br>這意味著<span style="background-color:yellow">房產總價（total_price）與面積（area） 之間關係密切</span>，面積越大，總價越高。
                                                <br>這是符合預期的。</p>
                    <p style='text-align: left;'>2. <span style="background-color:yellow">unit_price & age：相關係數約為 -0.43</span>，表現出中等強度的負相關。
                                                <br>說明房產單價（unit_price）隨著房齡（age）的增加而降低。<span style="background-color:yellow">房齡較大的房子單價可能相對較低。</span></p>
                    <p style='text-align: left;'>3. <span style="background-color:yellow">age & total_price</span>：相關係數為 -0.18，顯示出弱負相關，表示房齡較高的房產總價可能略低，但這種<span style="background-color:yellow">關係不強。</span></p>
                    <p style='text-align: left;'>4. <span style="background-color:yellow">unit_price & total_price</span>：相關係數為 0.34，顯示出弱到中等強度的正相關，意味著單價和總價之間存在一定程度的正相關關係，通常單價高的房產總價也較高，但<span style="background-color:yellow">影響程度不高。</span></p>
                    <p style='text-align: left;'>5. <span style="background-color:yellow">year、month 與其他變數</span>：年份和月份與其他變數的相關係數都非常小（接近 0），這意味著年份和月份對其他變數（例如總價、單價、面積等）幾乎沒有影響。 這可能是因為資料分佈在不同年份和月份的樣本變化不大，或者這些時間因素對價格和麵積等指標的<span style="background-color:yellow">影響並不顯著。</span></p>
                 """)   
    st.markdown("---")
    st.html("<h2  style='text-align:center;margin:0 0 3% 0'>== (KDD3) 交易數據轉換--</h2>")
    cols2 = st.columns([1, 1])
    cols2[0].subheader("1.產生的數據標籤")
    cols2[0].dataframe(selected_columns_with_index)
    cols2[1].subheader("2.說明")
    cols2[1].write('''
    * year：交易年份，由datetime轉化而來
    
    * month：交易月份，由datetime轉換而來
    
    * yq：交易年份和季度，由year&quarter轉換而來，2019Q1——2024Q1
    
    * quarter：交易季度，由month離散化而來
    
    * AR：屋齡範圍Age Range，由age離散化而來，分為 0-10,11-20,21-30,30-40 及 40年以上五個範圍
    ''')

    return X

def 季度模型(XXX):    ##== (KDD2)季度模型儀表板: Svyq = 總成交結構(X) ==##
    ##== (d).後台 ==##
    ##== (1).不同季度交易量

    Ta = pd.crosstab(XXX["地段"], XXX["yq"], margins=True);
    # start_period = pd.Period('2015Q1', freq='Q')
    ##== (2).頻次分布表
    Sv = pd.crosstab(index=XXX["地段"], columns=XXX["yq"],
                     values=XXX["unit_price"], aggfunc="mean", margins=True)


    FIGym = go.Figure(go.Scatter(x=Sv.T.index.astype(str), y=Sv.T["All"]))
    FIGym.update_traces(mode='markers+lines');
    FIGym.update_xaxes(tickformat='%Y-%m', dtick='M1');

    FIGym1 = px.pie(Ta[Ta.index != "All"], values="All", names=Ta[Ta.index != "All"].index, labels=Ta[Ta.index != "All"].index, color=Ta[Ta.index != "All"].index)


    fig = px.bar(Sv, x=Sv.index, y="All", color="All", text="All", barmode='group')

    fig1 = px.bar(Ta, x=Ta.index, y="All", color="All", text="All", barmode='group')

    # -- (B) 以下為 主畫面(canvas)設計
    st.markdown("---")
    st.header("== (KDD4) 交易模型（一）季度模型-- ")
    cols = st.columns([1, 1])  # -- (d).前台--canvas
    cols[0].subheader("1.1 四季度交易量")
    cols[0].dataframe(Ta)
    cols[1].subheader("1.2 交易量饼状图")
    cols[1].plotly_chart(FIGym1, theme="streamlit", use_container_width=True)
    st.subheader("1.3 數據解讀(KDD5) ")
    st.write('''   
        (1) 忠孝東路、吳興街、永吉路、信義路和基隆路等核心街道屬於信義區的蛋黃區,交易量明顯高於其他街道，顯示信義區的房地產需求主要集中在這些核心地段。這些街道往往有良好的交通接駁、商業設施和高生活機能，因此吸引了大部分買家。

        (2) 松山路、光復南路等街道雖然交易量不及核心街道，但仍具有一定市場需求，顯示出買家對價格和地段的平衡考量。

        (3) 位於邊緣的街道交易量較少，反映出需求較低，這些區域的購房可能主要來自於預算考量或特定社區的偏好，而非大眾市場需求。

        (4) 這張交易量圓餅圖反映出信義區房市需求的地理分布，顯示出購屋者偏好核心地帶，並逐漸向外擴展的趨勢,這對未來的房地產開發與市場定位具有參考價值。
        ''')
    st.markdown("---")
    cols1 = st.columns([1, 1])  # -- (d).前台--canvas
    cols1[0].subheader("2.1 四季度平均單價")
    cols1[0].dataframe(Sv)
    cols1[1].subheader("2.2 平均單價折線圖")
    cols1[1].plotly_chart(FIGym, theme="streamlit", use_container_width=True)
    st.subheader("2.3 數據解讀(KDD5)")
    st.write('''   
    (1) 從2019年到2021年的平均單價在70至75之間微幅波動但還算穩定，可能反映出當時房市需求相對穩定或供需平衡。雖然2020年初疫情爆發，可能對市場帶來一些影響，但由於疫情初期人們對經濟前景不確定，需求可能有所下降，因此價格並未顯著上升。
    
    (2) 隨著2021年疫情趨緩，需求開始快速釋放加上工作模式的改變，遠程辦公興起，相對富裕的買家選擇在都市核心區域購買更大或更高級的房產，以提升生活和工作的便利性，因此房價上漲。
    
    (3) 2022上半年價格持續上漲，推測是在2021年價格上漲之後，市場信心進一步增強，買家預期房價會繼續上漲，促使更多人搶購，形成了價格上漲的正向循環；2022下半年價格大幅下跌，推測可能是房市過熱、房價上漲過快導致部分買家選擇觀望或撤出市場。

    (4) 2023上半年雖然全球經濟環境充滿不確定因素，但部分購房需求仍然延續了疫情後的「報復性消費」模式,因此價格持續上漲；2023下半年，受到聯準會升息、地緣政治緊張(ex:中美競爭)、通膨、經濟不確定等因素影響，價格下跌。
    ''')

    return Sv

def 屋齡模型(XXX):

    AM = XXX.groupby("AR").agg({"地段": "nunique", "unit_price": "mean", "area":"count",
                                      }).reset_index()
    AM.columns = ["屋齡範圍","地段数","房單價","交易量"]

    # -- (B) 以下為 主畫面(canvas)設計
    st.markdown("---")
    st.header("== (KDD4) 交易模型（二）屋齡模型-- ")


    st.subheader("1. 屋齡交易量")
    st.dataframe(AM)

    st.subheader("2. 雷達圖")
    cols = st.columns([1, 1])  # -- (d).前台--canvas

    fig = px.funnel(AM, y="屋齡範圍", x="交易量", color="屋齡範圍", orientation="h")
    cols[0].subheader("2.1 不同屋齡範圍的交易量")
    cols[0].plotly_chart(fig, theme="streamlit", use_container_width=True)

    fig1 = px.funnel(AM, y="屋齡範圍", x="房單價", color="屋齡範圍", orientation="h")
    cols[1].subheader("2.2 不同屋齡範圍的房單價")
    cols[1].plotly_chart(fig1,theme="streamlit", use_container_width=True)
    st.subheader("3. 數據解讀(KDD5)")
    st.html('''
    <p>比較兩張圖:</p>
    <p>(1) <span style="background-color:yellow">屋齡對房屋購買有一定影響力</span>：新屋價格較高，但交易量低，顯示市場對價格敏感。隨著屋齡增加，<span style="background-color:yellow">價格下降，交易量增高</span>，許多買家偏好價格適中的房屋。</p>

    <p>(2) <span style="background-color:yellow">房屋價格隨屋齡增加而下降</span>，在<span style="background-color:yellow">(30,50)歲屋齡交易量達到高峰</span>，顯示部分買家願意購買屋齡較高的房屋以降低購房成本；<span style="background-color:yellow">50年以上屋齡的交易量下降</span>，反映市場對老屋需求低。</p>

    <p>(3) 無屋齡資料的房屋單價偏高，<span style="background-color:yellow">交易量排名第二</span>，可能位於特定地段或生活機能完善之處，即便無法判定屋齡，<span style="background-color:yellow">仍具高單價</span>。</p>

    <p>(4) 無屋齡資料的房屋單價偏高，推測是因為這些房屋包含了一些無法確認屋齡但價值較高的房產，或者位於特定地段的房屋，即便沒有屋齡資料，<span style="background-color:yellow">仍具有相對高的單價</span>。<p>

    <p>(5) <span style="background-color:yellow">屋齡越低單價越高</span>。****我對這個保有疑慮****</p>
        ''')

    return AM
    #AgeModel

# return places,number_df,unit_df,price_df
def select_option(df,places,usefor):
    option = st.selectbox("選擇一個選項", ['永吉路','信義路','基隆路','吳興街',
                                    '忠孝東路','虎林街','和平東路','嘉興街','松德路','松隆路','松仁路',
                                    '市民大道六段','福德街','富陽街','光復南路','松勤街','文昌街',
                                    '中坡南路','松平路','信安街','景雲街','松山路','紫雲街','崇德街',
                                    '東興路','松智路','中坡北路','莊敬路','松信路','仁愛路','松高路',
                                    '松勇路','逸仙路','大道路','林口街','青雲街','瑞雲街','祥雲街',
                                    '健康路'])
    st.write("您選擇了：", option)

    P,kind_P,P_age= 0,0,0
    p,kind_p,p_age= float("inf"),0,0
    show = []  
    length,place_price = [],[]
    ages = ["2~5", "6~10","11~20","20+"]

    # age
    for j,age in enumerate(ages):

        # i用來控制用途
        for i in range(5):
        
            length.append(len(df[(df["地段"]==places[option]) &(df["age"]==age) & (df["主要用途"]==int(i))]))
            place_price.append(df["total_price"][(df["地段"]==places[option]) &(df["age"]==age) & (df["主要用途"]==int(i))].sum())
            
            tmp = df["unit_price"][(df["地段"]==places[option]) &(df["age"]==age) & (df["主要用途"]==int(i))].sum()/len(df["unit_price"][(df["地段"]==places[option]) &(df["age"]==age) & (df["主要用途"]==int(i))])
            price_sum = df["unit_price"][(df["地段"]==int(0)) &(df["age"]==age) & (df["主要用途"]==int(i))].sum()
            number = len(df["unit_price"][(df["地段"]==places[option]) &(df["age"]==age) & (df["主要用途"]==int(i))])

            if P < tmp :
                P = tmp
                kind_P = i
                P_age = age
                P_number = number
            if p > tmp :
                p = tmp
                kind_p = i
                p_age = age
                p_number = number

    length = np.array(length).reshape(4,5)
    place_price = np.array(place_price).reshape(4,5)

    st.header(option+"段 每坪售出")
    P_heigh = '<p style="font-family:sans-serif; color:	SteelBlue; font-size: 20px;">最高 : %.2f 萬 ,用途 : %s ,屋齡 : %s 年 </p>'%(P,usefor[kind_P],P_age)
    st.markdown(P_heigh, unsafe_allow_html=True)
    P_low = '<p style="font-family:sans-serif; color:SlateGray; font-size: 20px;">最低 : %.2f 萬 ,用途 : %s ,屋齡 : %s 年 </p>'%(p,usefor[kind_p],p_age)
    st.markdown(P_low, unsafe_allow_html=True)
    fig = px.bar(df[df["地段"]==places[option]] , x="主要用途",y="total_price",
             color="age",
             barmode="group"
             #facet_row="time",
             #facet_col="day",
             #category_orders={"day": ["Thur","Fri","Sat","Sun"],"time":["Lunch", "Dinner"]}
            )
    place = df[df["地段"]==places[option]].copy()
    P = place[place['unit_price']==place['unit_price'].max()]
    p = place[place['unit_price']==place['unit_price'].min()]
    
    
    # 網頁上呈現
    st.plotly_chart(fig)
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 30px;">住家用 : 0 ,商業用 : 1 ,辦公用 : 2 ,住商用 : 3 ,工業用 : 4</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    st.text("p.s(其他用途通常為停車使用)")



    cols1 = st.columns([1,1])
    score_df = sumX(df,ages,length,usefor)
    score_df.set_index('屋齡', inplace=True)
    cols1[0].subheader("數量統計")
    cols1[0].write(score_df)
    
    unit_df = sumX(df,ages,place_price/length,usefor)
    unit_df.set_index('屋齡', inplace=True)
    cols1[1].subheader("平均單一物件金額")
    cols1[1].write(unit_df.style.highlight_max(axis=0))
    
    price_df = sumX(df,ages,place_price,usefor)
    price_df.set_index('屋齡', inplace=True)
    cols1[0].subheader("金額統計")
    cols1[0].dataframe(price_df.style.highlight_max(axis=0),width=600)
    


    location_price=[]
    unit_price=[]
    # 用來控地點
    for i,place in enumerate (places):
        # age
        for j,age in enumerate(ages):
            location_price.append(df["total_price"][(df["地段"]==i) &(df["age"]==age)].sum())
            unit_price.append(df["total_price"][(df["地段"]==i) &(df["age"]==age)].sum()/len(df["total_price"][(df["地段"]==i) &(df["age"]==age)]))
    location_price = np.array(location_price).reshape(len(places),4)
    unit_price = np.array(unit_price).reshape(len(places),4)

    place_age=[]
    unit_place_age=[]
    for j , p in enumerate (places):
        place_age.append({"地點":p,ages[0]:location_price[j][0], ages[1]:location_price[j][1],ages[2]:location_price[j][2],ages[3]:location_price[j][3]})
        unit_place_age.append({"地點":p,ages[0]:unit_price[j][0], ages[1]:unit_price[j][1],ages[2]:unit_price[j][2],ages[3]:unit_price[j][3]})

    place_age_df = pd.DataFrame(place_age)
    place_age_df.set_index('地點', inplace=True)
    unit_place_age_df = pd.DataFrame(unit_place_age)
    unit_place_age_df.set_index('地點', inplace=True)

    st.text("place_age_df")
    st.dataframe(place_age_df.style.highlight_max(axis=1))
    st.text("unit_place_age_df缺用途")
    st.dataframe(unit_place_age_df.style.highlight_max(axis=1))
    return places[option],score_df,unit_df,price_df

def 匯出PPT檔(PPTname):   ##== (KDD5) 匯出PPT檔(PPTname) ==##
    print(sss)
    #== (c1/d1).標題: 前台-canvas/前台-sidebar ==##
    st.header("(KDD5).匯出PPT檔案")
    st.sidebar.header("(KDD5).匯出PPT檔案");
    if st.sidebar.checkbox("* (KDD5) 匯出至 PPTX檔"):
        #== (b).後台-存檔 ==##
        sug_list = [ { "Ptitle": "謝謝", "Plist":  ["~~敬請指教!!"], "Plevel": [ 0 ] } ];    appendPPTX(sug_list)
        sss.prs.save(PPTname)
        #== (c2/d2).前台-canvas: 匯出 ==##
        st.subheader(f"* (KDD5) 匯出LOG 至PPT檔--{PPTname} --")
        st.write(f"* (KDD5) PPT檔--{PPTname} 己匯出")
        st.sidebar.write("* (KDD5) PPTX 己匯出")
        #== (c2/d2).前台-canvas: 匯出 ==##
        st.subheader("* PPT檔案結構 --")
        for slide_number, slide in enumerate(sss.prs.slides, start=1):
            title = None
            for shape in slide.shapes:
                if shape.has_text_frame:  title = shape.text
            if title: st.write(f"* [第{slide_number}頁] {title}")
            else:     st.write(f"* [第{slide_number}頁] 沒有標題")
    return

#%%##===== (W3).導航函式庫 =====#####
def check2log(textStr,log):      ##== check 再將 textStr 納入 log 中, 並中並可以提供建議 ==##
    st.sidebar.markdown('---')
    st.sidebar.header("== (KDD5)請用戶輸入解讀--")
    st.session_state.username = st.sidebar.text_input("", st.session_state.username, placeholder="輸入用戶名")
    sugg_key = f"log_checkbox_{len(log)}"
    suggestion = st.sidebar.text_area("", value=st.session_state.suggestion, key=sugg_key, height=20, placeholder="輸入建議")
    if st.sidebar.button("LOG操作 / 提交建議"):
        log.append(textStr)
        if st.session_state.username and suggestion:
            log.append(f"<{st.session_state.username}建議>> {suggestion}")
            st.sidebar.success("建议已提交并纳入LOG");     st.session_state.suggestion = ""
        else:
            st.sidebar.error("不列入建議,只單純LOG操作內容")
    return

def initSSS(variables, pjName):  ##== 初始化 state_session 的各變量 ==##
    sss = st.session_state
    if "LOG" not in sss:
        sss.LOG = [pjName]   #-- 初始化 LOG 列表
    if "username" not in sss:
        sss.username = ""    #-- 初始化 username 列表
    if "suggestion" not in sss:
        sss.suggestion = ""  #-- 初始化 suggestion 列表
    if "prs" not in sss:
        sss.prs = Presentation();     sss.prs = genPPTX(pjName, "date: " + str(date.today()))
    for var in variables:       #-- 初始化传入的变量名为 None
        if var not in sss: sss[var] = None
    return sss


# %%##===== (W3).本系統函式庫: (1)列印PPT,(2)導航 =====#####

# %%== (1).列印PPTX的函式庫: genPPTX(),addBulletPage(),addSlideDF(),makeDFtable() ==##
def genPPTX(mainTitle, subTitle):  ##== prs = genPPTX(mainTitle,subTitle): 產生一份新的投影片
    from pptx import Presentation
    prs = Presentation()
    slide0 = prs.slides.add_slide(prs.slide_layouts[0])
    slide0.shapes.title.text = mainTitle;
    slide0.placeholders[1].text = subTitle
    return prs


def addBulletPage(prs, Ptitle, Plist,
                  Plevel):  ##== prs = addBulletPage(prs,Ptitle,Plist,Plevel): 增加一個重點(Plist)頁,並設定重點層級(Plevel)及顏色 (Plevel=1)
    slide = prs.slides.add_slide(prs.slide_layouts[1]);  # -- 產生一頁(slide)新的 "標題與內容" 的重點頁(BulletPage)
    slide.shapes.title.text = Ptitle  # -- 設定標題(Ptitle)
    tf = slide.shapes.placeholders[1].text_frame  # -- 設定內文 文字框(tf)
    for k in np.arange(len(Plist)):
        if k == 0:
            tf.text = Plist[0]  # -- 設定第 1 子標題 (tf.text = Plist[0])
        else:  # -- 設定新增 子標題 (Plist[k]), 其層級 (Plevel[k]) 及顏色 (Plevel=1為粗體彩色)
            p = tf.add_paragraph();
            p.level = Plevel[k];
            p.text = Plist[k]
            if (p.level == 1):
                p.font.bold = True
                p.font.color.rgb = RGBColor(0, 0, 255)  # RGBColor(0xFF, 0x7F, 0x50)
    print("addBulletPage>>> generate Bullet Page-" + Ptitle)
    return prs


def addSlideDF(prs, ind, Ptable):  ##== prs = addSlideDF(prs,ind,Ptable): 將表格(Ptable)加入某頁 (prs.slides[ind])
    shapes = prs.slides[ind].shapes
    if (Ptable is not None):
        print("addSlideDF>>> generate dataframe Table...")
        left, top, width, height = Inches(1), Inches(1), Inches(8), Inches(6)
        table = shapes.add_table(Ptable.shape[0], Ptable.shape[1], left, top, width, height).table
        for i in np.arange(Ptable.shape[0]):
            for j in np.arange(Ptable.shape[1]):
                table.cell(i, j).text = str(list(Ptable.iloc[i])[j])
    return prs


def makeDFtable(df):  ##== table = makeDFtable(df): make df to table with first row as column names
    Xcol = pd.DataFrame(df.columns).transpose();
    Xcol.columns = df.columns;
    AAA = pd.concat([Xcol, df], axis=0);
    Arow = pd.DataFrame(AAA.index);
    Arow.index = Arow[Arow.columns[0]];
    BBB = pd.concat([Arow, AAA], axis=1);
    BBB.index = Arow[Arow.columns[0]]
    return BBB


# %%== (2).導航函式庫: appendPPTX(),check2log(),initSSS() ==##
def appendPPTX(rv_list):  ##== 以傳回數據(rv_list)生成投影片sss.prs ==##
    print(rv_list)
    with st.sidebar.expander("___ 當前投影片生成步驟 ....."):
        for i, rv in enumerate(rv_list):
            st.write(">> 生成投影片第" + str(len(sss.prs.slides) - 1) + "頁-" + rv.get("Ptitle") + " 中...")
            # st.sidebar.write(">> 生成"+rv.get("Ptitle")+"投影片中...")
            print(rv)
            if rv.get("Ptitle"): sss.prs = addBulletPage(sss.prs, rv.get("Ptitle"), rv.get("Plist"), rv.get("Plevel"))
            # if rv.get("df"):  sss.prs = addSlideDF(sss.prs, len(sss.prs.slides)-1, sss[rv.get("df")].head(2))
            if rv.get("df"):

                dfList = rv.get("df")
                for dfFile in dfList:  sss.prs = addSlideDF(sss.prs, len(sss.prs.slides) - 1,
                                                            makeDFtable(sss[dfFile].head(2)))
            if rv.get("table"):
                tblList = rv.get("table")
                for tbl in tblList:  sss.prs = addSlideDF(sss.prs, len(sss.prs.slides) - 1, makeDFtable(sss[tbl]))
            if rv.get("fig"):
                slide1 = sss.prs.slides[len(sss.prs.slides) - 1]
                picList = rv.get("fig")
                for picFile in picList:  pic1 = slide1.shapes.add_picture(picFile, Inches(1), Inches(
                    1));  # print(">>>>> 2."+picFile)
    return

#%%##===== (W4).網站架構 =====#####
if __name__ == "__main__":
    ##== (1).設定頁面組態 與 導航列 (前台(a)navbar) ==##
    st.set_page_config(page_title="SPC-S01 RDS系統", page_icon="✅", layout="wide",)  #==> [[AIp04/C4)(5)加上頁註,頁標題等]]
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    page = st_navbar(["[擷取交易]", "[季度模型]","[屋齡模型]","[路段選擇]","[匯出PPT檔]"])

    ##== (2).設定session初始值等 ==##
    Xname = "Xinyi.csv"
    df = "clean2.csv"
    sss = initSSS(["X", "TWH", "Svyq", "Xname","df"], "AIp03圖形可視化W"+"--"+Xname)
    sss.Xname = Xname
    sss.df = df
    df = pd.read_csv("clean3.csv")
    ##== (3).設定 前台((b)sidebar + (c)canvas)主標題 ==##
    title = '<h1 style="font-family:sans-serif;text-align:center;margin: 0 0 5% 0;">AIp04空間與網站: 初步運營分析儀表板(S01)</h1>'
    st.markdown(title, unsafe_allow_html=True)
    
    st.sidebar.title("初步運營分析(S01)控制盤--")


    places = {'永吉路':0,'信義路':1,'基隆路':2,'吳興街':3,'忠孝東路':4,'虎林街':5,'和平東路':6,'嘉興街':7,
              '松德路':8,'松隆路':9,'松仁路':10 ,'市民大道六段':11,'福德街':12,'富陽街':13,'光復南路':14,
              '松勤街':15,'文昌街':16,'中坡南路':17,'松平路':18,'信安街':19,'景雲街':20,'松山路':21,
              '紫雲街':22,'崇德街':23,'東興路':24,'松智路':25,'中坡北路':26,'莊敬路':27,'松信路':28,
              '仁愛路':29,'松高路':30,'松勇路':31,'逸仙路':32,'大道路':33,'林口街':34,'青雲街':35,
              '瑞雲街':36,'祥雲街':37,'健康路':38}
    usefor = {0:'住家用', 1:'商業用', 2:'辦公用', 3:'其他', 4:'住商用', 5:'工業用'}
    ##== (4).導航切換: 前台(a)navbar-->儀表板函式(b,c,d) ==##
    match page:
        case "[擷取交易]":
            sss.X = 擷取交易(sss.Xname)
            check2log(f"擷取交易: {sss.Xname} to get X with {sss.X.shape[0]} records", sss.LOG)
        case "[季度模型]":
            if sss.X is None:
                st.write("尚未擷取交易數據，請先擷取交易數據！")
                sss.LOG.append("尚未擷取交易數據，請先擷取交易數據！")
            else:
                sss.Svyq = 季度模型(sss.X)
                check2log(f"季度模型: Svyq with {sss.Svyq.shape} shape", sss.LOG)
        case "[屋齡模型]":
            if sss.X is None:
                st.write("尚未擷取交易數據，請先擷取交易數據！")
                sss.LOG.append("尚未擷取交易數據，請先擷取交易數據！")
            else:
                sss.Svyq = 屋齡模型(sss.X)
                check2log(f"屋齡模型: Svyq with {sss.Svyq.shape} shape", sss.LOG)

        case "[路段選擇]":
            if sss.df is None:
                st.write("尚未擷取交易數據，請先擷取交易數據！")
                sss.LOG.append("尚未擷取交易數據，請先擷取交易數據！")
            else:
                sss.Svyq = select_option(df,places,usefor)
                check2log(f"路段選擇: Svyq with {sss.Svyq[1].shape} shape", sss.LOG)
        case "[匯出PPT檔]":
            if sss.df is None:
                st.write("尚未擷取交易數據，請先擷取交易數據！")
                sss.LOG.append("尚未擷取交易數據，請先擷取交易數據！")
            else:
                匯出PPT檔("信义区房价分析.PPTX")

    ##== (5).操作日誌 ==##
    st.sidebar.markdown('<h2 style="color: blue;">操作LOG日誌</h2>', unsafe_allow_html=True)
    for i, log in enumerate(sss.LOG, 1): st.sidebar.write(f"({i}). {log}")