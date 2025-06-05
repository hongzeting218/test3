import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# 设置页面标题
st.title('心理健康与数字行为数据分析')

# 读取数据
@st.cache_data
def load_data():
    # 这里假设数据已经复制到mental_health_digital_behavior_data.csv文件中
    data = pd.read_csv('mental_health_digital_behavior_data.csv')
    return data

data = load_data()

# 显示原始数据
st.subheader('原始数据')
st.write(data)

# 数据可视化选择
st.sidebar.header('可视化选项')
chart_type = st.sidebar.selectbox(
    '选择图表类型',
    ['热力图', '散点图', '柱状图', '折线图', '箱线图']
)

# 热力图
if chart_type == '热力图':
    st.subheader('相关性热力图')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    
    st.write("""
    ### 热力图分析
    热力图显示了各变量之间的相关性。颜色越接近红色表示正相关性越强，
    颜色越接近蓝色表示负相关性越强。这有助于我们理解不同数字行为指标
    与心理健康指标之间的关系。
    """)

# 散点图
elif chart_type == '散点图':
    st.subheader('散点图分析')
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox('选择X轴变量', data.columns)
    with col2:
        y_axis = st.selectbox('选择Y轴变量', data.columns)
    
    color_by = st.selectbox('按变量着色(可选)', ['None'] + list(data.columns))
    
    if color_by == 'None':
        fig = px.scatter(data, x=x_axis, y=y_axis, 
                        title=f'{x_axis} vs {y_axis}')
    else:
        fig = px.scatter(data, x=x_axis, y=y_axis, color=color_by,
                        title=f'{x_axis} vs {y_axis} (按{color_by}着色)')
    
    st.plotly_chart(fig)
    
    st.write("""
    ### 散点图分析
    散点图可以直观地展示两个变量之间的关系。如果数据点呈现某种模式或趋势，
    表明这两个变量之间可能存在相关性。你可以尝试探索不同变量组合之间的关系。
    """)

# 柱状图
elif chart_type == '柱状图':
    st.subheader('柱状图分析')
    
    selected_column = st.selectbox('选择要分析的变量', data.columns)
    group_by = st.selectbox('分组变量(可选)', ['None'] + list(data.columns))
    
    if group_by == 'None':
        fig = px.histogram(data, x=selected_column, 
                          title=f'{selected_column}的分布')
    else:
        fig = px.histogram(data, x=selected_column, color=group_by,
                          title=f'{selected_column}按{group_by}分组')
    
    st.plotly_chart(fig)
    
    st.write("""
    ### 柱状图分析
    柱状图用于显示单个变量的分布情况。当添加分组变量时，可以比较不同组别之间的分布差异。
    这有助于我们理解数字行为指标或心理健康指标在不同人群中的分布特征。
    """)

# 折线图
elif chart_type == '折线图':
    st.subheader('折线图分析')
    
    st.write("""
    ### 折线图分析
    折线图适合展示变量随时间或其他有序变量的变化趋势。由于你的数据是横截面数据，
    我们可以展示某些变量的平滑趋势。
    """)
    
    selected_column = st.selectbox('选择要分析的变量', data.columns)
    
    # 为了展示折线图，我们需要一个有序变量，这里使用排序后的屏幕时间
    sorted_data = data.sort_values('daily_screen_time_min')
    
    fig = px.line(sorted_data, x='daily_screen_time_min', y=selected_column,
                 title=f'{selected_column}随屏幕时间的变化趋势')
    
    st.plotly_chart(fig)

# 箱线图
elif chart_type == '箱线图':
    st.subheader('箱线图分析')
    
    selected_column = st.selectbox('选择要分析的变量', data.columns)
    group_by = st.selectbox('分组变量(可选)', ['None'] + list(data.columns))
    
    if group_by == 'None':
        fig = px.box(data, y=selected_column, 
                    title=f'{selected_column}的分布')
    else:
        fig = px.box(data, x=group_by, y=selected_column,
                    title=f'{selected_column}按{group_by}分组')
    
    st.plotly_chart(fig)
    
    st.write("""
    ### 箱线图分析
    箱线图可以显示变量的分布情况，包括中位数、四分位数和异常值。
    当添加分组变量时，可以比较不同组别之间的分布差异。
    这有助于我们发现不同人群在数字行为或心理健康指标上的差异。
    """)

# 数据分析洞察
st.sidebar.header('数据分析洞察')
if st.sidebar.checkbox('显示数据分析洞察'):
    st.subheader('数据分析洞察')
    
    st.write("""
    ### 1. 屏幕时间与心理健康的关系
    - 通过热力图可以看到，每日屏幕时间(daily_screen_time_min)与数字健康评分(digital_wellbeing_score)呈负相关
    - 屏幕时间越长，数字健康评分越低，这可能表明过度使用设备对心理健康有负面影响
    """)
    
    st.write("""
    ### 2. 睡眠时间的影响
    - 睡眠时间(sleep_hours)与焦虑水平(anxiety_level)呈负相关
    - 充足的睡眠可能与较低的焦虑水平相关
    """)
    
    st.write("""
    ### 3. 应用切换次数
    - 应用切换次数(num_app_switches)与专注度评分(focus_score)呈负相关
    - 频繁切换应用可能会降低专注度
    """)
    
    st.write("""
    ### 4. 社交媒体使用时间
    - 社交媒体使用时间(social_media_time_min)与情绪评分(mood_score)的关系不明显
    - 需要进一步分析不同类型的社交媒体使用对情绪的影响
    """)