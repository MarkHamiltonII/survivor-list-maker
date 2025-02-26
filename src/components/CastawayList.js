import { useState } from "react";
import { DragDropContext, Draggable, Droppable } from "react-beautiful-dnd";
import CopyToClipboard from "react-copy-to-clipboard";
import { BsGripVertical, BsCheckLg } from "react-icons/bs";
import './CastawayList.css';

export default function CastawayList(props) {
    const { castawayList } = props;
    const [castaways, setCastaways] = useState(castawayList)
    const [buttonMessage, setButtonMessage] = useState()

    const onDragEnd = result => {
        const { destination, source } = result;

        if (!destination) {
            return;
        }

        if (destination.droppableId === source.droppableId && destination.index === source.index) {
            return;
        }

        const newCastaways = [...castaways];
        const movedCastaway = newCastaways.splice(source.index, 1);
        newCastaways.splice(destination.index, 0, movedCastaway[0]);

        setCastaways(newCastaways);
    }

    const copyToClipBoard = (castaways) => {
        let copyText = '';
        castaways.map((castaway, index) => {
            copyText += `${index + 1}. ${castaway.name} \n`
            return ''
        });
        copyText.slice(0, -2);
        return copyText;
    }

    const updateButtonMessage = () => {
        setButtonMessage(<div><BsCheckLg /> Rankings Copied!</div>)
        setTimeout(() => {
            setButtonMessage()
        }, 3000)
    }

    return (
        <div className="castaway-list-container">
            <h2>Season 48 Castaways</h2>
            <DragDropContext onDragEnd={onDragEnd}>
                <div className="draggable-table">
                    <Droppable droppableId="Table">
                        {(provided, snapshot) => (
                            <table ref={provided.innerRef} {...provided.droppableProps} className={`castaway-table isDraggingOver-${snapshot.isDraggingOver}`}>
                                <thead>
                                    <tr>
                                        <th>Rank</th>
                                        <th>Castaway</th>
                                        <th className="aux-info">Age</th>
                                        <th className="aux-info">Current Residence</th>
                                        <th className="aux-info">Occupation</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {castaways.map((castaway, index) => (
                                        <Draggable draggableId={`${index}`} index={index} key={index}>
                                            {(provided, snapshot) => (
                                                <tr ref={provided.innerRef} {...provided.draggableProps} className={snapshot.isDragging ? 'isDragging-' + snapshot.isDragging : 'bg-' + castaway.tribeColor} key={index} >
                                                    <td>{index + 1}</td>
                                                    <td><a href={castaway.pageURL} title={`${castaway.name}'s CBS page`} target="_blank" rel="noreferrer"><img src={castaway.iconURL} alt={`Portrait of ${castaway.name}`} /> <span>{castaway.name}</span></a></td>
                                                    <td className="aux-info">{castaway.age}</td>
                                                    <td className="aux-info">{castaway.currentResidence}</td>
                                                    <td className="aux-info">{castaway.occupation}</td>
                                                    <td {...provided.dragHandleProps}><BsGripVertical /></td>
                                                </tr>
                                            )}
                                        </Draggable>
                                    ))}
                                    {provided.placeholder}
                                </tbody>
                            </table>
                        )}
                    </Droppable>
                </div>
            </DragDropContext>
            <CopyToClipboard text={copyToClipBoard(castaways)}>
                <div className="copy-container">
                    <button className="copy-button" onClick={() => updateButtonMessage()}>
                        Copy your rankings!
                    </button>
                    <span className="copy-span">{buttonMessage}</span>
                </div>
            </CopyToClipboard>
        </div>
    )
}
