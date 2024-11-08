# Usage: streamlit run AIp05數據框轉換X.py --> http:/localhost:8501

import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder #, GridUpdateMode, JsCode, ColumnsAutoSizeMode
import plotly.express as px
import plotly.graph_objs as go

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties



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
    XXX["ym"] = pd.PeriodIndex(XXX.date, freq='M')

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
    # == (b).前台-sidebar ==##  #==> [[AIp04/C4)(2)垂直流程]]
    st.sidebar.header("== (KDD1)擷取交易數據 -- ")
    st.sidebar.write("* 交易檔名 = "+fname)
    st.sidebar.write("* 記錄筆數 = ", X.shape[0])
    ##== (c).前台-canvas ==##
    st.header("== (KDD1)擷取交易數據"+fname+" --")

    st.subheader("* 記錄筆數 = "+str(X.shape[0]))
    st.dataframe(X.head(5))
    
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

    # 热力图
    corr_matrix = X.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    
    
    
    # ==> [[AIp04/C4)(1)水平流程]]
    cols = st.columns([1, 1])  # -- (d).前台--canvas
    data_directions = '<h2 style="font-family:sans-serif;"text-align: center";">* %s 數據說明</p>'%fname
    cols[0].markdown(data_directions, unsafe_allow_html=True)
    cols[0].dataframe(df , width= 500)

    correlation_map = '<h2 style="font-family:sans-serif;">* Correlation</p>'
    cols[1].markdown(correlation_map, unsafe_allow_html=True)
    cols[1].pyplot(plt)
    cols[1].html("""<p style='text-align: left;'>1. <span style="background-color:yellow">total_price & area：相關係數接近 0.94</span>，表現出<span style="background-color:yellow">強烈的正相關</span>。
                                                <br>這意味著<span style="background-color:yellow">房產總價（total_price）與面積（area） 之間關係密切</span>，面積越大，總價越高。
                                                <br>這是符合預期的。</p>
                    <p style='text-align: left;'>2. <span style="background-color:yellow">unit_price & age：相關係數約為 -0.43</span>，表現出中等強度的負相關。
                                                <br>說明房產單價（unit_price）隨著房齡（age）的增加而降低。<span style="background-color:yellow">房齡較大的房子單價可能相對較低。</span></p>
                    <p style='text-align: left;'>3. <span style="background-color:yellow">age & total_price</span>：相關係數為 -0.18，顯示出弱負相關，表示房齡較高的房產總價可能略低，但這種<span style="background-color:yellow">關係不強。</span></p>
                    <p style='text-align: left;'>4. <span style="background-color:yellow">unit_price & total_price</span>：相關係數為 0.34，顯示出弱到中等強度的正相關，意味著單價和總價之間存在一定程度的正相關關係，通常單價高的房產總價也較高，但<span style="background-color:yellow">影響程度不高。</span></p>
                    <p style='text-align: left;'>5. <span style="background-color:yellow">year、month 與其他變數</span>：年份和月份與其他變數的相關係數都非常小（接近 0），這意味著年份和月份對其他變數（例如總價、單價、面積等）幾乎沒有影響。 這可能是因為資料分佈在不同年份和月份的樣本變化不大，或者這些時間因素對價格和麵積等指標的<span style="background-color:yellow">影響並不顯著。</span></p>
                 """)   


    
    

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
    st.header("== (KDD2) 交易季度模型-- ")

    cols = st.columns([1, 1])  # -- (d).前台--canvas
    cols[0].subheader("* 四季度交易量")
    cols[0].dataframe(Ta)
    cols[1].subheader("* 交易量饼状图")
    cols[1].plotly_chart(FIGym1, theme="streamlit", use_container_width=True)

    cols1 = st.columns([1, 1])  # -- (d).前台--canvas
    cols1[0].subheader("* 四季度平均單價")
    cols1[0].dataframe(Sv)
    cols1[1].subheader("* 平均單價折線圖")
    cols1[1].plotly_chart(FIGym, theme="streamlit", use_container_width=True)


    return Sv

def 屋齡模型(XXX):

    AM = XXX.groupby("AR").agg({"地段": "nunique", "unit_price": "mean", "area":"count",
                                      }).reset_index()
    AM.columns = ["屋齡範圍","地段数","房單價","交易量"]

    # -- (B) 以下為 主畫面(canvas)設計
    st.header("== (KDD3) 屋齡模型-- ")


    st.subheader("* 屋齡交易量")
    st.dataframe(AM)

    st.subheader("* 雷達圖")
    cols = st.columns([1, 1])  # -- (d).前台--canvas

    fig = px.funnel(AM, y="屋齡範圍", x="交易量", color="屋齡範圍", orientation="h")
    cols[0].subheader("不同屋齡範圍的交易量")
    cols[0].plotly_chart(fig, theme="streamlit", use_container_width=True)

    fig1 = px.funnel(AM, y="屋齡範圍", x="房單價", color="屋齡範圍", orientation="h")
    cols[1].subheader("不同屋齡範圍的房單價")
    cols[1].plotly_chart(fig1,theme="streamlit", use_container_width=True)
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

    for var in variables:       #-- 初始化传入的变量名为 None
        if var not in sss: sss[var] = None
    return sss

#%%##===== (W4).網站架構 =====#####
if __name__ == "__main__":
    ##== (1).設定頁面組態 與 導航列 (前台(a)navbar) ==##
    st.set_page_config(page_title="SPC-S01 RDS系統", page_icon="✅", layout="wide",)  #==> [[AIp04/C4)(5)加上頁註,頁標題等]]
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    page = st_navbar(["[擷取交易]", "[季度模型]","[屋齡模型]","[路段選擇]"])

    ##== (2).設定session初始值等 ==##
    Xname = "Xinyi.csv"
    df = "clean5.csv"
    sss = initSSS(["X", "TWH", "Svyq", "Xname","df"], "AIp03圖形可視化W"+"--"+Xname)
    sss.Xname = Xname
    sss.df = df
    df = pd.read_csv("clean5.csv")
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
    usefor = {0:'住家用', 1:'商業用', 2:'辦公用', 3:'住商用', 4:'工業用'}

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


    ##== (5).操作日誌 ==##
    st.sidebar.markdown('<h2 style="color: blue;">操作LOG日誌</h2>', unsafe_allow_html=True)
    for i, log in enumerate(sss.LOG, 1): st.sidebar.write(f"({i}). {log}")
# %%
