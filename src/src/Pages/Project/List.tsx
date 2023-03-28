import { useState } from 'react';
import { useQuery, useMutation } from '@apollo/client';
import { DateTime } from "luxon";

import { Badge, Table, TextInput, Card, Container, Modal, Text, Button, Anchor, ScrollArea, Group, ActionIcon, Skeleton } from '@mantine/core';
import { IconTrash } from '@tabler/icons';
import { GET_PROJECTS } from '../../graphql/queries';
import { DELETE_PROJECT, ADD_PROJECT } from '../../graphql/mutations';
import { Error } from '../../Components/Error';
import { Link } from 'react-router-dom';


export function ProjectsPage() {
  const { loading, error, data } = useQuery(GET_PROJECTS);
  const [deleteProject] = useMutation(DELETE_PROJECT, {
    refetchQueries: [{ query: GET_PROJECTS }],
    onCompleted() {
      setDeleteProjectId(0);
    }
  });
  const [addProject, addData] = useMutation(ADD_PROJECT, {
    refetchQueries: [{ query: GET_PROJECTS }],
    onCompleted() {
      setProjectName("");
      setAddProjectOpened(false);
    }
  });
  const [deleteProjectId, setDeleteProjectId] = useState(0);
  const [addProjectOpened, setAddProjectOpened] = useState(false);
  const [projectName, setProjectName] = useState("");
  let rows = null;

  const openDeleteDialog = (projectId: number) => {
    setDeleteProjectId(projectId);
  };

  const closeDeleteDialog = () => {
    setDeleteProjectId(0);
  };

  const doDeleteProject = () => {
    deleteProject({
      variables: {
        projectId: deleteProjectId
      }
    });
  };

  const closeAddProjectDialog = () => {
    setAddProjectOpened(false);
  };

  const openAddDialog = () => {
    setAddProjectOpened(true);
  };

  const doCreateProject = () => {
    addProject({
      variables: {
        name: projectName
      }
    });
  };

  const doSetProjectName = (event: any) => {
    setProjectName(event.target.value);
  };

  const maybeSubmit = (e: any) => {
    if (e.keyCode === 13) {
      doCreateProject();
    }
  };

  if (data) {
    rows = data.projects.list.map((row: any) => {
      return (
        <tr key={row.id}>
          <td><Anchor component={Link} to={`/dashboard/project/${row.id}`}>{row.name}</Anchor></td>
          <td>
            <Badge color={"green"}>{row.plan.slug}</Badge> {row.plan.requestsPerMonth.toLocaleString()} reqs/month.
          </td>
          <td>
            {DateTime.fromISO(row.createdAt).toLocaleString(DateTime.DATETIME_MED)}
          </td>
          <td>
            <Group spacing={0} position="right">
              <ActionIcon onClick={() => openDeleteDialog(row.id)} color="red">
                <IconTrash size={16} stroke={1.5} />
              </ActionIcon>
            </Group>
          </td>
        </tr>
      );
    });
  }
  return (
    <ScrollArea>
      <Group align="flex-end">
        <h2 style={{ flex: 1 }} >Projects</h2>
        <Button my={20} onClick={openAddDialog} color={"green"}>Add</Button>
      </Group>

      <Modal opened={!!deleteProjectId} title="Delete project" withCloseButton onClose={closeDeleteDialog} size="lg" radius="md">
        <Text size="sm" mb="xs" weight={500}>
          Are you sure to delete project?
        </Text>

        <Group align="flex-end">
          <Button color={"red"} onClick={doDeleteProject}>Delete</Button>
        </Group>
      </Modal>

      <Modal opened={addProjectOpened} title="Add new project" withCloseButton onClose={closeAddProjectDialog} size="lg" radius="md">
        <Error text={addData?.error?.toString()} />
        <Group align="flex-end">
          <TextInput autoFocus onKeyDown={maybeSubmit} required sx={{ flex: 1 }} onChange={doSetProjectName} value={projectName} />
          <Button color={"green"} loading={addData.loading} onClick={doCreateProject}>Add</Button>
        </Group>
      </Modal>

      { loading ? (
        <>
          <Skeleton height={8} mt={6} radius="xl" />
          <Skeleton height={8} mt={6} radius="xl" />
          <Skeleton height={8} mt={6} radius="xl" />
        </>
      ) : (
        <>
        { error ? (
          <Error text={error?.toString()} />
        ) : (
          <Container>
            { rows && rows.length ? (
              <Table sx={{ minWidth: 800 }} verticalSpacing="xs">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Plan</th>
                    <th>Created At</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>{rows}</tbody>
              </Table>
            ) : (
              <Card>No projects. Please add one to get credentials.</Card>
            )}
          </Container>
        )}
        </>
      )}
    </ScrollArea>
  );
}