import { makeAutoObservable } from "mobx";


export class Wallet {
  address: string = "";

  constructor() {
    makeAutoObservable(this);
  }

  setAddress(address: string) {
    this.address = address;
  }
}
