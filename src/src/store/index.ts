import { createContext, useContext } from "react";
import { User } from "./User";
import { Wallet } from "./Wallet";

let user = new User();
let wallet = new Wallet();

const store = {
  user: user,
  wallet: wallet
};

export const StoreContext = createContext(store);

export const useStore = () => {
  return useContext<typeof store>(StoreContext);
};

export default store;
