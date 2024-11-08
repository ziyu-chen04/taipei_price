import streamlit as st
import pandas as pd
import plotly_express as px
import numpy as np
def main(df,places,usefor):
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
    ages = ["2~5", "6~10","11~20","20+"]

    for i in range(6):
        for j,age in enumerate(ages):
            tmp = df["total_price"][(df["地段"]==places[option]) &(df["age"]==age) & (df["主要用途"]==int(i))].sum()/len(df["total_price"][(df["地段"]==places[option]) &(df["age"]==age) & (df["主要用途"]==int(i))])
            price_sum = df["total_price"][(df["地段"]==int(0)) &(df["age"]==age) & (df["主要用途"]==int(i))].sum()
            number = len(df["total_price"][(df["地段"]==places[option]) &(df["age"]==age) & (df["主要用途"]==int(i))])
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
    
    st.header(option+"段 每坪售出")
    
    st.text("最高 : %.2f 元 ,用途 : %s ,屋齡 : %s 年 ,售出數量: %s" %(P,usefor[kind_P],P_age,P_number))
    st.text("最低 : %.2f 元 ,用途 : %s ,屋齡 : %s 年 ,售出數量: %s" %(p,usefor[kind_p],p_age,p_number))
    fig = px.bar(df[df["地段"]==places[option]] , x="主要用途",y="total_price",
             color="age",
             barmode="group",
             #facet_row="time",
             #facet_col="day",
             #category_orders={"day": ["Thur","Fri","Sat","Sun"],"time":["Lunch", "Dinner"]}
            )
    # 網頁上呈現
    st.plotly_chart(fig)
    st.text("住家用 : 0 ,商業用 : 1 ,辦公用 : 2 ,其他 : 3 ,住商用 : 4 ,工業用 : 5")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("一只猫")
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.header("一只狗")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("一只猫头鹰")
        st.image("https://static.streamlit.io/examples/owl.jpg")

        
    
    data = np.random.randn(10, 1)

    # "对象" 方法 编写
    data1, data2 = st.columns([3, 1])    # 设置左右布局大小为3:1
    data1.subheader("一个宽容器，含有图表")
    data1.line_chart(data)

    data2.subheader("一个窄容器，含有数据")
    data2.write(data)
    
    return df



if __name__ == '__main__':
    #raw = pd.read_csv("Xinyi.csv")
    #df = pd.read_csv("clean1.csv")
    df2 = pd.read_csv("clean2.csv")
    #df3 = pd.read_csv("clean3.csv")
    places = {'永吉路':0,'信義路':1,'基隆路':2,'吳興街':3,'忠孝東路':4,'虎林街':5,'和平東路':6,'嘉興街':7,
              '松德路':8,'松隆路':9,'松仁路':10 ,'市民大道六段':11,'福德街':12,'富陽街':13,'光復南路':14,
              '松勤街':15,'文昌街':16,'中坡南路':17,'松平路':18,'信安街':19,'景雲街':20,'松山路':21,
              '紫雲街':22,'崇德街':23,'東興路':24,'松智路':25,'中坡北路':26,'莊敬路':27,'松信路':28,
              '仁愛路':29,'松高路':30,'松勇路':31,'逸仙路':32,'大道路':33,'林口街':34,'青雲街':35,
              '瑞雲街':36,'祥雲街':37,'健康路':38}
    usefor = {0:'住家用', 1:'商業用', 2:'辦公用', 3:'其他', 4:'住商用', 5:'工業用'}
    main(df2 , places,usefor)