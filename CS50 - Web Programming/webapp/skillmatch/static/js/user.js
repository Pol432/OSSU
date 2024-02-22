const options = {
    responsive: true,
    legend: {
        position: 'right',
    }
};

function start(){
    fetch(`/user_view`)
    .then(response => response.json())
    .then(data => {
        let user_data = data;
        if (user_data.done_test){
            const percentages = [user_data.mechanic, user_data.scientific, user_data.persuasive, user_data.artistic, user_data.calculus];
            create_chart(percentages);
        }
        console.log(user_data)
        
        const savedProjects = document.getElementById("saved-projects")
        ReactDOM.render(<Projects projects={user_data.saved_projects}/>, savedProjects)

        if (data.user_type == "teacher") {
            const createdProjects = document.getElementById("created-projects")
            ReactDOM.render(<Projects projects={user_data.created_projects}/>,  createdProjects)
        }
    })
}

function create_chart(percentages) {
    const info = {
        labels: ["Mechanic", "Scientific", "Persuasive", "Artistic", "Calculus"],
        datasets: [
            {
                label: "My Dataset",
                data: percentages,
                backgroundColor: ["#38BAB1", "#2523AF", "#9A39C3", "#D935CA", "#3F23CB"],
                borderWidth: 1,
            },
        ],
    };
    const ctx = document.getElementById("myChart").getContext("2d");
    const myChart = new Chart(ctx, {
        type: "pie",
        data: info,
        options: options,
    });
}

class Projects extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            projects: [],
        };
    }

    componentDidMount() {
        Promise.all(
            this.props.projects.map((projectID) =>
                fetch(`/project_view/${projectID}`).then((response) => response.json())
            )
        ).then((projects) => {
            this.setState({ projects });
        });
    }

    handleClick(project) {
        if (project.pending) { 
            alert("Your project is still pending revision, try again later.");
            return;
        }
        window.location.href = `/project/${project.id}`;
    }

    render() {
        return (
            <div className="projects">
                {this.state.projects.map((project, index) => (
                    <div 
                        onClick={() => this.handleClick(project)} 
                         className="project"
                    >
                        <h3> {project.name} </h3>
                    </div>
                ))}
            </div>
        );
    }
}


document.addEventListener("DOMContentLoaded", start())