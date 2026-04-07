import ChatBox from "../components/ChatBox";

const Chat = ({ selectedChat }: any) => {
    return (
        <div style={{padding: "20px" }}>
            <ChatBox selectedChat={selectedChat} />
        </div>
    );
};

export default Chat;
