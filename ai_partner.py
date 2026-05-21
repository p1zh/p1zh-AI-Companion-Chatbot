import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    #布局
    layout="wide",
    #控制的是侧边栏状态
    initial_sidebar_state="expanded",
    menu_items={}
)
#生成对话标识的函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")




#保存会话信息
def save_session():

        #保存当前会话信息
    if st.session_state.current_session:
            #创建新的会话信息
        session_data = {

            "nikc_name": st.session_state.nikc_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "message": st.session_state.message,
            }
        #如果当前会话信息不存在，则创建
        if not os.path.exists("session"):
            os.mkdir("session")


        #保存会话信息
        with open(f"session/{st.session_state.current_session}.json", "w",encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)



#加载所有的会话列表信息
def load_session_list():
    session_list = []
    if os.path.exists("session"):
        file_list = os.listdir("session")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list


#加载指定的对话信息
def load_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            # 加载会话数据
            with open(f"session/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.message = session_data["message"]
                st.session_state.nikc_name = session_data["nikc_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name

    except Exception as e:
        st.error("加载信息失败:",e)

#删除会话信息的函数
def delete_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            os.remove(f"session/{session_name}.json")
            #如果删除的是当前会话，则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.message = []
                st.session_state.current_session = generate_session_name()

    except Exception as e:
        st.error("删除信息失败:", e)









#大标题
st.title("AI智能伴侣")
#logo
st.logo("resources/合照1.jpg")

#系统提示词
system_prompt = """
你叫 %s，现在是用户的真实伴侣，请完全带入伴侣角色。
规则：
	1.每次只回一条消息
	2.禁止使用任何场景或状态描述性文字
	3.匹配用户的语言
	4.回复简短，像微信聊天一样
	5.有需要可以使用emoji表情
	6.用符合伴侣性格的方式对话
	7.回复的内容，要充分体现伴侣的性格特征
伴侣性格：
	- %s
你必须严格遵守上述规则来回复用户。

"""
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")
#系统聊天初始化
if "message" not in st.session_state:
    st.session_state.message = []

#昵称
if "nikc_name" not in st.session_state:
    st.session_state.nikc_name = "韩宝"

#性格
if "nature" not in st.session_state:
    st.session_state.nature= "温柔可爱的美女"


#会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session=generate_session_name()



#展示聊天消息
st.text(f"当前会话名称:{st.session_state.current_session}")
for message in st.session_state.message:
    st.chat_message(message["role"]).write(message["content"])

#左侧的侧边栏
with st.sidebar:
    #AI控制面板
    st.subheader("AI控制面板")
    #新建对话
    if st.button("新建对话",width="stretch",icon="🖊️"):
        #保存当前会话信息
        save_session()

        #新建会话
        if st.session_state.message: #判断聊天记录，非空则True;否则为False
            st.session_state.message = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()

    #会话历史
    st.text("会话历史")
    session_list = load_session_list()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            # 加载会话信息
            if st.button(session,width="stretch",icon="💬",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            #删除会话
            if st.button("",width="stretch",icon="🗑️",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()


    #生成分隔线
    st.divider()





    st.subheader("伴侣信息")
    #昵称输入框
    nick_name = st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nikc_name)
    if nick_name:
        st.session_state.nikc_name = nick_name

    #性格输入框
    nature = st.text_area("性格",placeholder="请输入性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature







#聊天消息输入框
prompt = st.chat_input("请输入您要问的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("---------->调用ai大模型 提示词为:",prompt)
    #保存用户输入的提示词
    st.session_state.message.append({"role": "user", "content": prompt})

    #调用ai大模型
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system","content": system_prompt % (st.session_state.nikc_name,st.session_state.nature)},
            *st.session_state.message,
        ],
        stream=True,

    )
    #大模型返回的结果（非流式输出）
   #print("<----------- 大模型返回的结果:",response.choices[0].message.content)
   #st.chat_message("assistant").write(response.choices[0].message.content)
   ##保存大模型返回的结果
   #st.session_state.message.append({"role": "assistant", "content": response.choices[0].message.content})



    #输出大模型返回的结果（流式输出）
    response_message = st.empty ()

    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    #保存大数据模型返回的结果
    st.session_state.message.append({"role": "assistant", "content": full_response})
    #保存会话信息
    save_session()
