import { createContext, useContext } from "react";
import { User } from "./User";

let user = new User();

const store = {
  user: user
};

export const StoreContext = createContext(store);

export const useStore = () => {
  return useContext<typeof store>(StoreContext);
};

export default store;
