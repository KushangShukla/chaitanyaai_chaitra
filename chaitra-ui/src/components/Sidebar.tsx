const Sidebar=({ setPage }) => {
    return (
        <div style={{
            width:"250px",
            background:"#0f172a",
            color:"white",
            height:"100vh",
            padding:"20px"
        }}>
            <h2>CHAITRA</h2>

            <div onClick={() => setPage("chat")}>Chat</div>
            <div onClick={() => setPage("dashboard")}>Dashboard</div>
            <div onClick={() => setPage("profile")}>Profile</div>
        </div>
    );
};

export default Sidebar;