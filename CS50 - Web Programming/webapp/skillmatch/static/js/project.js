function start() {
    var general = document.getElementById("actions");
    ReactDOM.render(<Action/>, general)
}

class Action extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: null,
            likes: null,
            added: null,
            liked: null
        };
    }

    componentDidMount() {
        const project = document.getElementById("project");
        const id = project.getAttribute("data-projectID")

        fetch(`/project_view/${id}`)
        .then(response => response.json())
        .then(data => {
            this.setState({
                id: id,
                likes: data.likes, 
                added: data.added, 
                liked: data.liked
            })
        })
    }

    updateLikes(projectId) {
        fetch(`/update_likes/${projectId}`)
        .then(response => response.json())
        .then(data => {
            this.setState({likes: data.likes, liked: data.liked})
        })
    }

    addProject(projectId) {
        fetch(`/add_project/${projectId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie("csrftoken")
        }
        }).then(response => response.json())
        .then(data => {
            this.setState({added: data.added})
        })
    }      
    

    render () {
        return(
            <div class="action-container">
                <div class="h_container">
                    <i  id="heart" onClick={() => this.updateLikes(this.state.id)} 
                        class="far fa-heart"
                        style={{color: this.state.liked ? "red" : "white"} }></i>
                    <h4> {this.state.likes} </h4>
                </div>
                <button type="submit" onClick={() => this.addProject(this.state.id)}> 
                    {this.state.added ? "ADDED" : "ADD PROJECT"} 
                </button>
            </div>
        )
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
}

document.addEventListener("DOMContentLoaded", start());

/* 

            <div class="action-container">
                <div class="h_container">
                    <i id="heart" class="far fa-heart"></i>
                    <h4> {{ project.likes }} </h4>
                </div>
                <button type="submit"> ADD PROJECT </button>
            </div>
*/