import { useEffect, useState } from 'react'

/** Animacion de escritura simple: va revelando el texto caracter a caracter. */
export default function Typewriter({ text, speed = 25, className = '' }) {
    const [shown, setShown] = useState('')
    const done = shown.length >= text.length

    useEffect(() => {
        setShown('')
        let i = 0
        const id = setInterval(() => {
            i += 1
            setShown(text.slice(0, i))
            if (i >= text.length) clearInterval(id)
        }, speed)
        return () => clearInterval(id)
    }, [text, speed])

    return (
        <p className={className}>
            {shown}
            {!done && <span className="animate-pulse">▌</span>}
        </p>
    )
}
