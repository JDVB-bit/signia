import { useState } from 'react'

function Button({children, variant = "default", onClick}){
    const styles = {
        primary: '',
        secondary: '',
        sidebar: '',
        burble: '',
        stop: '',
        default: ''
    }
    
    return (
        <button className={styles[variant]} onClick={onClick}>
            {variant === 'sidebar' ? (
                <span className=''></span>
            ) : (
                children
            )}
        </button>
    )
}

export default Button