// import React from "react";
// import styles from "./page.module.css";
//
// interface Props {
//   children?: React.ReactNode;
// }
//
// const Button: React.FC<Props> = ({ children }) => {
//   return <button className={styles.button}>{children}</button>;
// };
//
// export default Button;
//

import React from "react";
import "./Button.css";  

interface Props {
  children?: React.ReactNode;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  type?: "button" | "submit" | "reset";
}

const Button = ({ onClick, children, type = "button" }: Props) => {
  return (
    <button onClick={onClick} className="button" type={type}>
      {children}
    </button>
  );
};

export default Button;
