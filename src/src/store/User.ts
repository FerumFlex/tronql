import { Md5 } from 'ts-md5';
import { makeAutoObservable } from "mobx";


export class UserData {
  planSlug: string;

  constructor(planSlug: string) {
    this.planSlug = planSlug;
  }
}


export class UserProperties {
  id: string;
  active: boolean;
  data: UserData | null = null;
  email: string;
  verified: boolean;

  constructor(id: string, active: boolean, email: string, verified: boolean, data: UserData | null) {
    this.id = id;
    this.active = active;
    this.data = data;
    this.email = email;
    this.verified = verified;
  }

  get username() : string {
    return this.email;
  }

  getImageUrl(size: number) : string {
    if (! this.email) {
      return `https://www.gravatar.com/avatar/00000000000000000000000000000000?s=${size.toString()}`;
    }
    return `https://www.gravatar.com/avatar/${Md5.hashStr(this.email)}?s=${size.toString()}`;
  }
}

export class User {
  props: UserProperties | null = null;
  isLoading: boolean = true;

  constructor() {
    makeAutoObservable(this);
  }

  setData(data: any) {
    this.isLoading = false;
    if (data) {
      this.props = new UserProperties(
        data.id,
        data.active,
        data.email,
        data.verified,
        new UserData(data.data.planSlug),
      );
    } else {
      this.props = null;
    }
  }

  logOut() {
    localStorage.setItem("token", "");
    localStorage.setItem("refreshToken", "");
    this.props = null;
  }

  get isLoggedIn() : boolean {
    return !!this.props;
  }
}
