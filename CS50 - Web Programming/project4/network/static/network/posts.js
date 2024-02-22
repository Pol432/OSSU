var counter = 0;
const quantity = 10;

document.addEventListener("DOMContentLoaded", load("next"));

function load(dir) {
    let end;
    let start;
    if (dir == "next") {
        end = counter + quantity - 1;
        start = counter;
        counter = end + 1;
    } else if (dir == "previous") {
        end = (counter + quantity - 1) - 9;
        start = counter - 9;
        counter = end + 1;
    }

    let posts = document.getElementById("posts");
    let next_button = "";
    let previous_button = "";
    let url_dir = posts.getAttribute("data-value");
   
    fetch(`/${url_dir}?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        if (end < Object.keys(data.posts).length) { 
            next_button = document.getElementById("load_next");
        }
        if (start != 0) { 
            previous_button = document.getElementById("load_previous"); 
        }

        posts.innerHTML = "";
        data.posts.forEach(add_post);

        posts.append(next_button); 
        posts.append(previous_button);
    })
}

function add_post(content) {
    const post = document.createElement("div");
    post.setAttribute("id", content.id)  
    document.querySelector("#posts").prepend(post);
    
    ReactDOM.render(<Post content={content} />, document.getElementById(content.id))
}

class Post extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            author: null,
            user: null,
            isLoading: true
        };
    }

    componentDidMount() {
        const post = this.props.content;
        fetch(`/post_view/${post.id}`)
        .then(response => response.json())
        .then(data => {
            this.setState({ author: data.author,
                            user: data.user,
                            isLoading: false, })
        })
    }

    render() {
        const post = this.props.content;
        let edit = "";

        if (this.state.isLoading) {
            return <div> Loading... </div>
        }
        
        if (this.state.user != "") {
            if (this.state.author.id == this.state.user.id) {
                edit = <EditButton post={post} />;
            }
        }

        let href = `/profile/${this.state.author.id}`
        return (
            <div class="post_container">
                <a href={ href }>
                    <h4> { this.state.author.username } </h4>
                </a>
                { edit }
                <p> { post.content } </p>
                <p> { post.date } </p>
                <p>&hearts; { post.likes } </p> 
            </div>
        );
    }
}

function EditButton(props) {
    return (
        <button onClick={() => {
            editPost(props.post);
        }}>
            Edit
        </button>
    );
}

function editPost(post) {
    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    post.csrfmiddlewaretoken = csrf_token;

    fetch("edit_post", {
        method: "POST",
        body: JSON.stringify(post),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
    .then(response => response.text())
    .then(html => {
        document.querySelector("#page_content").innerHTML = html;
    });
}