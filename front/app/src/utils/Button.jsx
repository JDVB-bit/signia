import { useState } from 'react'

function Button({children, variant = "default", onClick}){
    const styles = {
        // Solo los 5 colores de la paleta: primary usa "secondary" (el color
        // alterno para resaltar) de fondo con "brand-inverso" (texto
        // alterno) encima; secondary usa "surface" (el color secundario) de
        // fondo con "brand" (el color de texto normal) encima.
        primary: 'rounded-md bg-secondary px-8 py-4 text-base font-semibold text-brand-inverso transition-opacity hover:opacity-90',
        secondary: 'rounded-md bg-surface px-8 py-4 text-base font-semibold text-brand transition-opacity hover:opacity-90',
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