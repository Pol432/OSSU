const NULL = {"id": 0, "positive": [], "negative": [], "instruction": ""} // NULL activity

var areas = {
    "mechanic": 0,
    "scientific": 0,
    "persuasive": 0,
    "artistic": 0,
    "calculus": 0
}
var kuder_content, holland_test;
var activityGroups = [];

function quiz() {
    kuder_content = document.getElementById("kuderContent");
    holland_test = document.getElementById("hollandTest");
    const loadingDiv = <h3> Cargando... </h3>;
    ReactDOM.render(loadingDiv, kuder_content);

    fetch(`/test_view`)
      .then(response => response.json())
      .then(data => {
        data.test.forEach((activities, id) => {
            activityGroups.push(<ActivityGroup id={id} activities={activities}/>);
        })
        renderGroup(0);
    });
}

function renderGroup(id) {
    let activity_group = activityGroups[id];
    kuder_content.classList.add('fadeOut');
    setTimeout(() => {
        ReactDOM.unmountComponentAtNode(kuder_content);
        ReactDOM.render(activity_group, kuder_content);
        kuder_content.classList.remove('fadeOut');
        kuder_content.classList.add('fadeIn');
        setTimeout(() => {
            kuder_content.classList.remove('fadeIn');
        }, 750);
    }, 750);
}

// edit areas only for the activities
function editAreas(list, action) {
    let operation = (action == "remove") ? -1 : 1;

    for (let i = 0; i < list.length; i++) {
        if (areas.hasOwnProperty(list[i])) {
            areas[list[i]] += operation;
        }
    }
}


class ActivityGroup extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: props.id,
            activities: props.activities,
            selectedPositive: NULL,
            selectedNegative: NULL
        };
    }

    handleClick(activity, type) {
        let keys = (type == "Positive") 
            ? {"selected": "selectedPositive", "opposite": "selectedNegative"} 
            : {"selected": "selectedNegative", "opposite": "selectedPositive"};
        let types = (type == "Positive") 
            ? {"selected": "positive", "opposite": "negative"} 
            : {"selected": "negative", "opposite": "positive"};
        
        if (this.state[keys.opposite].id == activity.id) { // If the opposite of the current activity is selected
            editAreas(this.state[keys.opposite][types.opposite], "remove");
            this.setState({ [keys.opposite]: NULL })
        } else if (this.state[keys.selected].id == activity.id) { // If it is clicked again when activity was already selected
            editAreas(activity[types.selected], "remove");
            this.setState({ [keys.selected]: NULL })
            return;
        // Else if another activty was already selected
        } else if (this.state[keys.selected] != NULL) { editAreas(this.state[keys.selected][types.selected], "remove"); } 
        this.setState({ [keys.selected]: activity });
        editAreas(activity[types.selected], "add");
        this.forceUpdate();
    }

    render() {
        let id = this.props.id;
        let { selectedPositive, selectedNegative } = this.state;
        let listActivities = this.props.activities.map(activity => {
            let className = "activity";
            if (selectedPositive.id === activity.id) {
              className += " selected-positive";
            } else if (selectedNegative.id === activity.id) {
              className += " selected-negative";
            }
            return (
            <div className={className}>
                <button
                    className={className == "activity" ? "unselected" : "selected"}
                    onClick={() => this.handleClick(activity, "Negative")}> - </button>
                <p className={className == "activity" ? "unselected" : "selected"}>{activity.instruction}</p>
                <button
                    className={className == "activity" ? "unselected" : "selected"}
                    onClick={() => this.handleClick(activity, "Positive")}> + </button>
            </div>);
        });
        const hasPrevious = id > 0;
        const hasNext = id < activityGroups.length - 1;
        const disabledNext = (selectedNegative == NULL || selectedPositive == NULL);

        const previousButton = hasPrevious && (
            <button className="switchButton" style={{ float: "left" }} onClick={() => renderGroup(id-1)}>
                Anterior
            </button>);
        const nextButton = hasNext ?
            (<button className="switchButton" style={{float: "right"}} disabled={disabledNext} onClick={()=>renderGroup(id+1)}>
                Siguiente
            </button>): 
            (<button className="switchButton" style={{float: "right"}} disabled={disabledNext} onClick={renderHolland}>
                Siguiente
            </button>)
            
        return( 
            <div id={"activityGroup" + id.toString()} className="activityGroup">
                <h4> Group {id + 1} of {activityGroups.length} </h4>
                {listActivities} {previousButton} {nextButton} 
            </div>
        );
    }
}

document.addEventListener("DOMContentLoaded", quiz());