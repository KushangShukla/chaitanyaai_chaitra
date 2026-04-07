import ChatBox from "../components/ChatBox";

const Chat = ({ selectedChat, onMessageSent }: any) => {
    return (
        <div style={{padding: "20px" }}>
            <ChatBox selectedChat={selectedChat} onMessageSent={onMessageSent} />
        </div>
    );
};

export default Chat;
