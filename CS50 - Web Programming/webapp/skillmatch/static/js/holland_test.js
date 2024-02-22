

var kuder_test;
var holland_content;

function renderHolland() {
    const {t} = useTranslation();
    holland_test.style.removeProperty("display");
    holland_test = document.getElementById("hollandTest");
    kuder_test = document.getElementById("kuderTest");
    kuder_test.classList.add('fadeOut');
    holland_test.classList.add('fadeOut');
    setTimeout(() => {
        kuder_test.remove();
        holland_test.style.removeProperty("display");
        holland_test.classList.remove('fadeOut');
        holland_test.classList.add('fadeIn');
        setTimeout(() => {
            holland_test.classList.remove('fadeIn');
        }, 750);
    }, 750);
    holland_content = document.getElementById("hollandContent");
    ReactDOM.render(<CharacteristicList />, holland_content);
}


function renderSecond() {
    holland_content.classList.add("fadeOut");
    setTimeout(() => {
        ReactDOM.unmountComponentAtNode(holland_content);
        ReactDOM.render(<Personality />, holland_content);
        holland_content.classList.remove('fadeOut');
        holland_content.classList.add('fadeIn');
        setTimeout(() => {
            holland_content.classList.remove('fadeIn');
        }, 750);
    }, 750);
}


function submitTest() {
    holland_content.classList.add("fadeOut");
    setTimeout(() => {
        ReactDOM.unmountComponentAtNode(holland_content);
        const loadingDiv = <h3> Cargando... </h3>;
        ReactDOM.render(loadingDiv, holland_content);
        fetch('/test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie("csrftoken")
            },
            body: JSON.stringify({ areas })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                ReactDOM.unmountComponentAtNode(holland_content);
                ReactDOM.render(<FinalMessage />, holland_content);
            }
        })
        holland_content.classList.remove('fadeOut');
        holland_content.classList.add('fadeIn');
        setTimeout(() => {
            holland_content.classList.remove('fadeIn');
        }, 750);
    }, 750);
}


class FinalMessage extends React.Component {
    render() {
        return (
            <div class="submitMessage">
                <h4> ¡Thanks for finishing this test! </h4>
                <p> To continue to the main page click <a href="/"> here </a> </p>
            </div>
        );
    }
}


class Personality extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            clicked: []
        };
    }
    
    handleClick(area) {
        this.setState(prevState => {
            const clicked = [...prevState.clicked];
            const index = clicked.indexOf(area);
            if (index >= 0) {
                clicked.splice(index, 1);
                editAreasCharacteristics(area, "remove", second_areas);
            } else {
                clicked.push(area);
                editAreasCharacteristics(area, "add", second_areas);
            }
            return { clicked };
        });
    }

    render() {
        return (
            <div>
                <h3> Group 2 of 2 </h3>
                    <p> Select the adjectives that descrive your personality. Try to define yourself as you are, not as you would like to be. Choose at least 3 </p>

                <div className="adjective-grid">
                    {second_questions.map((charac, index) => (
                        <button className={(this.state.clicked.includes(charac.area)) ? "adjective-clicked": ""} 
                                onClick={() => this.handleClick(charac.area)}>{charac.adjective}</button>
                    ))}
                </div>
                <button
                    className="switchButton" style={{ float: "right" }} disabled={!(this.state.clicked.length > 0)} 
                    onClick={submitTest}>
                    Siguiente
                </button>
            </div>
        );
    }
}


class CharacteristicList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            allClicked: false
        };
    }

    handleChildClick = () => {
        const allClicked = first_questions.every(charac => charac.componentRef.state.tdClicked > 0);
        this.setState({ allClicked });
    };

    render() {
        const { allClicked } = this.state;
        return (
            <div id="firstQuestions">
                <h3> Group 1 of 2 </h3>
                <p> Click on the box that you consider yourself to be compared to other people of your age according to the following characteristics. </p>
                <div class="firstQuestions">
                    <table class="firstContent">
                        <thead>
                            <tr>
                                <th class="characteristic"> Característica </th>
                                <th> Más que los demás </th>
                                <th> Igual que los demás  </th>
                                <th> Menos que los demás </th>
                            </tr>
                        </thead>
                        {first_questions.map((charac, index) => (
                            <Characteristic
                                charac={charac.carac}
                                area={charac.area}
                                onChildClick={this.handleChildClick}
                                ref={el => (charac.componentRef = el)}/>
                        ))}
                    </table>
                </div>
                <button className="switchButton" style={{ float: "right" }} disabled={!allClicked} onClick={renderSecond}>
                    Siguiente
                </button>
            </div>
        );
    }
}

class Characteristic extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tdClicked: 0
        };
    }

    handleTdClick = (id) => {
        if (id == 1) {
            if (this.state.tdClicked == 1) {
                editAreasCharacteristics(this.props.area, "remove", first_areas);
                this.setState({ tdClicked: 0 })
                return;
            }
            editAreasCharacteristics(this.props.area, "add", first_areas);
            this.setState({ tdClicked: 1 }, () => this.props.onChildClick());
            return;
        }
        this.setState({ tdClicked: id }, () => this.props.onChildClick());
    };

    render() {
        const { charac } = this.props;
        const { tdClicked } = this.state;
        return (
            <tr class="characteristic">
                <td> {charac} </td>
                <td
                    className={1 === tdClicked ? "td1Clicked" : ""}
                    onClick={() => this.handleTdClick(1)}></td>
                <td
                    className={2 === tdClicked ? "td2Clicked" : ""}
                    onClick={() => this.handleTdClick(2)}></td>
                <td
                    className={3 === tdClicked ? "td3Clicked" : ""}
                    onClick={() => this.handleTdClick(3)}></td>
            </tr>
        );
    }
}

function editAreasCharacteristics(area, action, question_area) {
    let operation = (action == "remove") ? -1 : 1;

    for (let key in question_area) {
        if (question_area[key].includes(area)) {
            areas[question_areas[key]] += operation;
            console.log(question_areas[key]);
        }
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
}