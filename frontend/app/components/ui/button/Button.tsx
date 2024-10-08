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

import styles from "./Button.module.css";

interface Props {
  children?: React.ReactNode;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  type?: "button" | "submit" | "reset";
}

const Button = ({ onClick, children, type = "button" }: Props) => {
  return (
    <button onClick={onClick} className={styles.button} type={type}>
      {children}
    </button>
  );
};
export default Button;

//
// import React, { FC } from "react";
//
// import styles from "./page.module.css";
//
// interface Props {
//   children?: React.ReactNode;
//   onClick?: React.MouseEventHandler<HTMLButtonElement>;
//   type?: "button" | "submit" | "reset";
// }
//
// const Button: FC<Props> = ({ onClick, children, type = "button" }) => {
//   return (
//     <button onClick={onClick} className={styles.button} type={type}>
//       {children}
//     </button>
//   );
// };
// export default Button;
