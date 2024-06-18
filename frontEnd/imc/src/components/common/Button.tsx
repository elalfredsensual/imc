//create a button component wich recieves a text and a function to execute when clicked
const Button = ({text, onClick}: {text: string, onClick: () => void}) => {
    return (
        <button onClick={onClick}>{text}</button>
    )
}

export { Button }