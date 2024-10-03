import React from "react";
import styles from "./page.module.css";

interface Props {
  children?: React.ReactNode;
  onClick?: React.ReactEventHandler;
  type?: any;
}

const Button = ({ onClick, children, type }: Props) => {
  return (
    <button onClick={onClick} className={styles.button} type={type}>
      {children}
    </button>
  );
};
export default Button;
