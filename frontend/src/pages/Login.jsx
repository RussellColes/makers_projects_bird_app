import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/authentication";
import pluckerIcon from "../assets/icon/pluckers.png";
import "./Login.css";

import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";


export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

    localStorage.clear()
    const navigate = useNavigate();
    
    async function handleSubmit(event) {
        event.preventDefault();
        try {
            // login() sets items in localStorage
            await login(email, password)
            navigate("/myprofile")
        } catch (err) {
            console.error(err);
            toast.error("Invalid login: Please check your email and password");
            navigate("/login");
        }
    }
    
    function handleEmailChange(event) {
        setEmail(event.target.value);
    }
    
    function handlePasswordChange(event) {
        setPassword(event.target.value);
    }

  return (
    <div className="wrapper-auth">
    <ToastContainer toastStyle={{ backgroundColor: "#E4E0E1", color: "#493628" }}/>
    <div className='home-container'>
        <div className="app-name-container">
          <h1>Plucker</h1>
        </div>
      <div className='plucker-logo'>
        <img src={pluckerIcon} alt='Plucker logo' />
      </div>
      <div className='login-container'>
        <h2>Login</h2>
        <form
          className='login-form'
          action='/login'
          method='POST'
          onSubmit={handleSubmit}>
          <label className='username'>Email</label>

          <br></br>
          <input
            type='email'
            id='email'
            name='email'
            placeholder='Email'
            value={email}
            onChange={handleEmailChange}
          />
          <br></br>
          <label className='password'>Password</label>
          <br></br>
          <input
            type='password'
            id='password'
            name='password'
            placeholder='Password'
            value={password}
            onChange={handlePasswordChange}
          />
          <br></br>
          <div className='buttons-container'>
            <button
              type='submit'
              className='submit-button'
              role='submit-button'
              id='submit'>
              Login
            </button>
            <br></br>
            <button
              type='button'
              className='submit-button'
              role='submit-button'
              id='signup'
              onClick={() => navigate("/SignUp")}>
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
    </div>
  );
}

//     return (
//         
//         <div className="home-container">
//         {/* <NavBar /> */}
//         <div className="name-container">
//             <div className="plucker-logo"><img src={pluckerIcon} alt="Plucker logo" /></div>
//             <h1>Plucker</h1><h2>Where watching birds is cool!</h2></div>
//         <div className="login-container">
//             <h2>Login</h2>
//             <form className="login-form" action="/login" method="POST" onSubmit={handleSubmit}>
//                 <label className="email_address">Email address</label>

//                 <br></br>
//                 <input 
//                     type="email" 
//                     id="email" 
//                     name="email" 
//                     placeholder="Email address"
//                     value={ email }
//                     onChange={handleEmailChange} />
//                 <br></br>
//                 <label className="password">Password</label>
//                 <br></br>
//                 <input 
//                     type="text" 
//                     id="password" 
//                     name="password" 
//                     placeholder="Password"
//                     value={ password }
//                     onChange={handlePasswordChange} />
//                 <br></br>
//                 <div className="buttons-container">
//                 <input 
//                     type="submit" 
//                     value="Login"
//                     className="submit-button"
//                     role="submit-button"
//                     id="submit" />
//                 <br></br>
//                 <button 
//                     type="button"
//                     className="signup-redirect"
//                     id="signup-button" 
//                     onClick={() => window.location.href = '/signup'}>
//                     Signup
//                 </button>
//                 </div>
//             </form>
//         </div>
//         </div>
//         </div>
//     )
// }
