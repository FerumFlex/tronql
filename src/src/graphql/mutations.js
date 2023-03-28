import { gql } from '@apollo/client';


export const EDIT_PROJECT = gql`
  mutation editProject($projectId: Int!, $name: String!) {
    editProject(projectId: $projectId, name: $name) {
      id
      token
      name
    }
  }
`;


export const DELETE_PROJECT = gql`
  mutation deleteProject($projectId: Int!) {
    deleteProject(projectId: $projectId) {
      id
      token
      name
    }
  }
`;


export const ADD_PROJECT = gql`
  mutation addProject($name: String!) {
    addProject(name: $name) {
      id
      token
      name
    }
  }
`;


export const VERIFY_EMAIL = gql`
  mutation verifyEmail($form: VerifyEmailFormInput!) {
    verifyEmail(form: $form)
  }
`;


export const LOGIN = gql`
  mutation login($form: LoginFormInput!) {
    login(form: $form) {
      refreshToken
      token
      tokenExpirationInstant
      user {
        id
        active
        data {
          planSlug
        }
        firstName
        lastName
        email
      }
    }
  }
`;


export const REFRESH_TOKEN = gql`
  mutation refreshToken($form: RefreshTokenFormInput!) {
    refreshToken(form: $form) {
      refreshToken
      token
    }
  }
`;


export const SIGNUP = gql`
  mutation signup($form: SignupFormInput!) {
    signup(form: $form) {
      token
      tokenExpirationInstant
      user {
        id
        active
        verified
        data {
          planSlug
        }
        email
        firstName
        lastName
      }
      refreshToken
    }
  }
`;


export const FORGOT_PASSWORD = gql`
  mutation forgotPassword($form: ForgotPasswordFormInput!) {
    forgotPassword(form: $form)
  }
`;


export const CHANGE_PASSWORD = gql`
  mutation changePassword($form: ChangePasswordFormInput!) {
    changePassword(form: $form)
  }
`;
