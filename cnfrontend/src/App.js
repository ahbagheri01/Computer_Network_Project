import React from 'react';
import logo from './logo.svg';
import './App.css';

const LoginRegisterMenu = ({state, setState}) => {
  return (
    <>
      <h1>Welcome</h1>
      <div>
        <h2>Sign up user</h2>
        Username: <input type="text" id="user_signup_username" /> <br/>
        Password: <input type="password" id="user_signup_password" /> <br/>
        <button onClick={() => {
          const username = document.getElementById('user_signup_username').value;
          const password = document.getElementById('user_signup_password').value;
          console.log(username, password);
        }}>Sign up</button> <br />

        <h2>Login user</h2>
        Username: <input type="text" id="user_login_username" /> <br/>
        Password: <input type="password" id="user_login_password" /> <br/>
        <button onClick={() => {
          const username = document.getElementById('user_login_username').value;
          const password = document.getElementById('user_login_password').value;
          console.log(username, password);
        }}>Login</button> <br />

        <h2>Sign up admin</h2>
        Username: <input type="text" id="admin_signup_username" /> <br/>
        Password: <input type="password" id="admin_signup_password" /> <br/>
        <button onClick={() => {
          const username = document.getElementById('admin_signup_username').value;
          const password = document.getElementById('admin_signup_password').value;
          console.log(username, password);
        }}>Sign up</button> <br />

        <h2>Login admin</h2>
        Username: <input type="text" id="admin_login_username" /> <br/>
        Password: <input type="password" id="admin_login_password" /> <br/>
        <button onClick={() => {
          const username = document.getElementById('admin_login_username').value;
          const password = document.getElementById('admin_login_password').value;
          console.log(username, password);
        }}>Login</button> <br />

        <h2>Login manager</h2>
        Username: <input type="text" id="manager_login_username" /> <br/>
        Password: <input type="password" id="manager_login_password" /> <br/>
        <button onClick={() => {
          const username = document.getElementById('manager_login_username').value;
          const password = document.getElementById('manager_login_password').value;
          console.log(username, password);
        }}>Login</button> <br />
      </div>
    </>
  );
}

const UserMenu = ({state, setState}) => {
  return (
    <>
      <h1>Welcome, admin!</h1> 
      <button onClick={() => {
        // todo
      }}>Upload video</button><br />

      <button onClick={() => {
        // todo
      }}>See list of all videos</button>
      <h2>All videos</h2>
      <ul>
          {
            state.videos.map(video => {
              return <li>ID: {video.id} - Name: {video.name} - User: {video.username} - Number of likes: {video.numberOfLikes} - Number of dislikes: {video.numberOfDislikes}</li>
            })
          }  
      </ul>
      <h2>See video</h2>
      Video ID: <input type="text" id="see_video_user_id" /> <br/>
      <button onClick={() => {
        const videoId = document.getElementById('see_video_user_id').value;
        console.log(videoId);
      }}>See video</button><br />

      <h2>Like video</h2>
      Video ID: <input type="text" id="like_video_id" /> <br/>
      <button onClick={() => {
        const videoId = document.getElementById('like_video_id').value;
        console.log(videoId);
      }}>Like video</button><br />

      <h2>Dislike video</h2>
      Video ID: <input type="text" id="dislike_video_id" /> <br/>
      <button onClick={() => {
        const videoId = document.getElementById('dislike_video_id').value;
        console.log(videoId);
      }}>Dislike video</button><br />

      <h2>See comments for a video</h2>
      Video ID: <input type="text" id="see_comments_video_id" /> <br/>
      <button onClick={() => {
        const videoId = document.getElementById('see_comments_video_id').value;
        console.log(videoId);
      }}>See comments for a video video</button><br />

      <h2>Add comment for a video</h2>
      Video ID: <input type="text" id="add_comment_video_id" /> <br/>
      Comment: <input type="text" id="add_comment_text" /> <br/>
      <button onClick={() => {
        const videoId = document.getElementById('add_comment_video_id').value;
        const comment = document.getElementById('add_comment_text').value;
        console.log(videoId, comment);
      }}>Add comment for a video</button><br />

      <button onClick={() => {
        // todo
      }}>See all tickets between user and admin, with answers</button>
      <h2>All user-admin tickets</h2>
      <ul>
          {
            state.userToAdminTickets.map(ticket => {
              return <li>ID: {ticket.id} - State: {ticket.state} - Content: '{ticket.content}' - Answer: '{ticket.answer}'</li>
            })
          }  
      </ul>
      <h2>Send ticket</h2>
      Content: <input type="text" id="send_ticket_user_to_admin_content" /> <br/>
      <button onClick={() => {
        const ticketContent = document.getElementById('send_ticket_user_to_admin_content').value;
        console.log(ticketContent);
      }}>Send ticket</button><br />

      <button onClick={() => {
        // todo
      }}>Logout</button>
    </>
  )
}

const AdminMenu = ({state, setState}) => {
  return (
    <>
      <h1>Welcome, admin!</h1> 
      <button onClick={() => {
        // todo
      }}>See list of all videos</button>
      <h2>All videos</h2>
      <ul>
          {
            state.videos.map(video => {
              return <li>ID: {video.id} - Name: {video.name} - User: {video.username} - Number of likes: {video.numberOfLikes} - Number of dislikes: {video.numberOfDislikes}</li>
            })
          }  
      </ul>
      <h2>See video</h2>
      Video ID: <input type="text" id="see_video_id" /> <br/>
      <button onClick={() => {
        const videoId = document.getElementById('see_video_id').value;
        console.log(videoId);
      }}>See video</button><br />
      <h2>Add danger tag</h2>
      Video ID: <input type="text" id="danger_tag_video_id" /> <br/>
      <button onClick={() => {
        const videoId = document.getElementById('danger_tag_video_id').value;
        console.log(videoId);
      }}>Add danger tag</button><br />
      <h2>Remove video</h2>
      Video ID: <input type="text" id="remove_video_id" /> <br/>
      <button onClick={() => {
        const videoId = document.getElementById('remove_video_id').value;
        console.log(videoId);
      }}>Remove video</button><br />
      <h2>Remove user's strike</h2>
      Username: <input type="text" id="remove_strike_username" /> <br/>
      <button onClick={() => {
        const username = document.getElementById('remove_strike_username').value;
        console.log(username);
      }}>Remove user's strike</button><br />

      <button onClick={() => {
        // todo
      }}>See all tickets between user and admin, with answers</button>
      <h2>All user-admin tickets</h2>
      <ul>
          {
            state.userToAdminTickets.map(ticket => {
              return <li>ID: {ticket.id} - State: {ticket.state} - Content: '{ticket.content}' - Answer: '{ticket.answer}'</li>
            })
          }  
      </ul>
      <h2>Answer ticket</h2>
      ID: <input type="text" id="answer_ticket_user_to_admin_id" /> <br/>
      Content: <input type="text" id="answer_ticket_user_to_admin_answer" /> <br/>
      <button onClick={() => {
        const ticketID = document.getElementById('answer_ticket_user_to_admin_id').value;
        const ticketAnswer = document.getElementById('answer_ticket_user_to_admin_answer').value;
        console.log(ticketID, ticketAnswer);
      }}>Send answer</button><br />


      <button onClick={() => {
        // todo
      }}>See all tickets between admin and manager, with answers</button>
      <h2>All admin-manager tickets</h2>
      <ul>
          {
            state.adminToManagerTickets.map(ticket => {
              return <li>ID: {ticket.id} - State: {ticket.state} - Content: '{ticket.content}' - Answer: '{ticket.answer}'</li>
            })
          }  
      </ul>
      <h2>Send ticket to manager</h2>
      Content: <input type="text" id="send_ticket_admin_to_manager_content" /> <br/>
      <button onClick={() => {
        const ticketContent = document.getElementById('send_ticket_admin_to_manager_content').value;
        console.log(ticketContent);
      }}>Send ticket</button><br />

      <button onClick={() => {
        // todo
      }}>Logout</button>
    </>
  )
}

const ManagerMenu = ({state, setState}) => {
  return (
    <>
      <h1>Welcome, manager!</h1>
      <button onClick={() => {
        // todo
      }}>Show list of waiting admins</button>
      <h2>Waiting admins list</h2>
      <ul>
          {
            state.waitingAdminUsernames.map(admin => {
              return <li>{admin}</li>
            })
          }  
      </ul>
      <button onClick={() => {
        // todo
      }}>Show list of accepted admins</button>
      <h2>Accepted admins list</h2>
      <ul>
          {
            state.acceptedAdminUsernames.map(admin => {
              return <li>{admin}</li>
            })
          }  
      </ul>
      <h2>Accept admin</h2>
      Username: <input type="text" id="accept_admin_username" /> <br/>
      <button onClick={() => {
        const username = document.getElementById('accept_admin_username').value;
        console.log(username);
      }}>Accept admin</button> <br />
      <h2>Set proxy details for admin</h2>
      Proxy username: <input type="text" id="proxy_admin_proxy_username" /> <br/>
      Proxy password: <input type="text" id="proxy_admin_proxy_password" /> <br/>
      Admin username: <input type="text" id="proxy_admin_admin_username" /> <br/>
      <button onClick={() => {
        const proxyUsername = document.getElementById('proxy_admin_proxy_username').value;
        const proxyPassword = document.getElementById('proxy_admin_proxy_password').value;
        const adminUsername = document.getElementById('proxy_admin_admin_username').value;
        console.log(proxyUsername, proxyPassword, adminUsername);
      }}>Set proxy details for admin</button> <br />

      <button onClick={() => {
        // todo
      }}>See all tickets between admin and manager, with answers</button>
      <h2>All admin-manager tickets</h2>
      <ul>
          {
            state.adminToManagerTickets.map(ticket => {
              return <li>ID: {ticket.id} - State: {ticket.state} - Content: '{ticket.content}' - Answer: '{ticket.answer}'</li>
            })
          }  
      </ul>
      <h2>Answer ticket</h2>
      ID: <input type="text" id="answer_ticket_admin_to_manager_id" /> <br/>
      Content: <input type="text" id="answer_ticket_admin_to_manager_answer" /> <br/>
      <button onClick={() => {
        const ticketID = document.getElementById('answer_ticket_admin_to_manager_id').value;
        const ticketAnswer = document.getElementById('answer_ticket_admin_to_manager_answer').value;
        console.log(ticketID, ticketAnswer);
      }}>Send answer</button><br />

      <button onClick={() => {
        // todo
      }}>Logout</button>
    </>
  )
}

function App() {
  const [state, setState] = React.useState({
    token: "",
    currentState: 1, // 0 = login/register menu, 1 = user logged in, 2 = admin logged in, 3 = manager logged in
    videos: [],
    comments: [],
    waitingAdminUsernames: [],
    acceptedAdminUsernames: [],
    userToAdminTickets: [],
    adminToManagerTickets: [],
  });

  return (
    <div style={{padding: 20}}>
      {state.currentState === 0 && <LoginRegisterMenu state={state} setState={setState} />}
      {state.currentState === 1 && <UserMenu state={state} setState={setState} />}
      {state.currentState === 2 && <AdminMenu state={state} setState={setState} />}
      {state.currentState === 3 && <ManagerMenu state={state} setState={setState} />}
    </div>
  );
}

export default App;
