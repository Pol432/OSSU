var converter = new showdown.Converter();
var projectsContent;

function initialize() {
    projectsContent = document.getElementById("content");
    const loadingDiv = <h3 class="project"> Cargando... </h3>;
    ReactDOM.render(loadingDiv, projectsContent);
    fetch(`/projects_view`)
      .then(response => response.json())
      .then(data => {
        ReactDOM.unmountComponentAtNode(projectsContent);
        ReactDOM.render(<Projects projects={data.projects}/>, projectsContent);
      });
}

class Projects extends React.Component {
    handleClick(id) {
        window.location.href = `/project/${id}`;
    }

    render() {
        return (
            <div className="projects">
                {this.props.projects.map((project, index) => (
                    <div data-aos="fade-up" data-aos-once="true" data-aos-duration="750" className="project" key={index}>
                        <div className="img-container">
                            <img src={project.img} />
                        </div>
                        <div className="content" onClick={() => this.handleClick(project.id)}>
                            <div className="main-container">
                                <h3>{project.name}</h3>
                                <div className="summary">
                                    <p> {project.introduction} </p>
                                </div>
                            </div>
                            <div className="generalInfo">
                                <h4>Related Careers:</h4>
                                <ul>
                                    {project.careers.slice(0, 2).map((career, index) => (
                                        <li key={index}>{career}</li>
                                    ))}
                                </ul>
                                <h4 id="abilities">Abilities you will Develop:</h4>
                                <ul id="abilities">
                                    {project.abilities.slice(0, 2).map((ability, index) => (
                                        <li key={index}>{ability}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }
}

document.addEventListener("DOMContentLoaded", initialize());