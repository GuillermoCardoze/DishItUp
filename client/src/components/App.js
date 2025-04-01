import { useContext, useState } from "react";
import { UserContext } from "./UserContext";
import Login from "./Login";
import Signup from "./Signup";

function App() {
    const { user, logout, loading } = useContext(UserContext);
    const [showSignup, setShowSignup] = useState(false);

    if (loading) return <h1>Loading...</h1>;

    return (
        <div>
            {user ? (
                <>
                    <h1>Welcome, {user.username}!</h1>
                    <button onClick={logout}>Logout</button>
                </>
            ) : (
                <>
                    {showSignup ? <Signup /> : <Login />}
                    <p>
                        {showSignup ? "Already have an account?" : "Don't have an account?"}{" "}
                        <button onClick={() => setShowSignup(!showSignup)}>
                            {showSignup ? "Login" : "Sign Up"}
                        </button>
                    </p>
                </>
            )}
        </div>
    );
}

export default App;
