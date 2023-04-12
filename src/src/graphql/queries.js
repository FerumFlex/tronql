import { gql } from '@apollo/client';

export const ME = gql`
  query me {
    me {
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
  }
`;


export const GET_PROJECTS = gql`
  query getProjects {
    projects {
      list {
        id
        name
        token
        createdAt
        plan {
          id
          slug
          createdAt
          updatedAt
          requestsPerMonth
          rateLimit
          ratePeriod
        }
      }
      count
    }
  }
`;


export const GET_PROJECT = gql`
  query getProject($projectId: Int!, $begin: DateTime!, $end: DateTime!, $begin2: DateTime!) {
    project(projectId: $projectId) {
      id
      name
      token
      createdAt
      plan {
        id
        slug
        createdAt
        updatedAt
        requestsPerMonth
        rateLimit
        ratePeriod
      }
      currentStats {
        total
      }
    }

    getStats(projectId: $projectId, end: $end, begin: $begin) {
      date
      count
    }

    dayStats: getStats(projectId: $projectId, end: $end, begin: $begin2, group: day) {
      date
      count
    }
  }
`;
