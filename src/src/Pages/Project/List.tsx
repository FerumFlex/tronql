import { useState } from 'react';
import { useQuery, useMutation } from '@apollo/client';

import { rem, Progress, Center, createStyles, Badge, SegmentedControl, Table, TextInput, Card, Container, Modal, Text, Button, Anchor, ScrollArea, Group, ActionIcon, Skeleton, FocusTrap } from '@mantine/core';
import { IconTrash } from '@tabler/icons';
import { GET_PROJECTS } from '../../graphql/queries';
import { DELETE_PROJECT, ADD_PROJECT } from '../../graphql/mutations';
import { Error } from '../../Components/Error';
import { Link } from 'react-router-dom';


const useStyles = createStyles((theme) => ({
  root: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.white,
    boxShadow: theme.shadows.md,
    border: `${rem(1)} solid ${
      theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[1]
    }`,
  },

  indicator: {
    backgroundImage: theme.fn.gradient({ from: 'pink', to: 'orange' }),
  },

  control: {
    border: '0 !important',
  },

  label: {
    '&, &:hover': {
      '&[data-active]': {
        color: theme.white,
      },
    },
  },
  progressBar: {
    '&:not(:first-of-type)': {
      borderLeft: `${rem(3)} solid ${
        theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.white
      }`,
    },
  },
}));


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
  const [network, setNetwork] = useState("tron-mainnet");
  const { classes, theme } = useStyles();
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
        name: projectName,
        networkSlug: network
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

  const setNetworkEvent = (value: string) => {
    setNetwork(value);
  };

  let networks = [];
  if (data) {
    rows = data.projects.list.map((row: any) => {
      let totalUsedPercent = (row.currentStats.total / row.plan.requestsPerMonth) * 100;
      return (
        <tr key={row.id}>
          <td><Anchor component={Link} to={`/dashboard/project/${row.id}`}>{row.name}</Anchor></td>
          <td>
            <Badge color={"green"}>{row.plan.slug}</Badge> {row.plan.requestsPerMonth.toLocaleString()} reqs/month.
          </td>
          <td>
            <Badge color={"blue"} title={row.network.title}>{row.network.slug}</Badge>
          </td>
          <td>
            <Progress
              classNames={{ bar: classes.progressBar }}
              sections={[
                {
                  value: totalUsedPercent,
                  color: theme.colorScheme === 'dark' ? theme.colors.red[9] : theme.colors.red[6],
                },
                {
                  value: 100 - totalUsedPercent,
                  color: theme.colorScheme === 'dark' ? theme.colors.teal[9] : theme.colors.teal[6],
                },
              ]}
            />
          </td>
          <td>
            <Group spacing={0} position="right">
              <ActionIcon onClick={() => openDeleteDialog(parseInt(row.id))} color="red">
                <IconTrash size={16} stroke={1.5} />
              </ActionIcon>
            </Group>
          </td>
        </tr>
      );
    });
    for (let row of data.networks) {
      networks.push({
        "label": row.title,
        "value": row.slug
      });
    }
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
        <FocusTrap active={addProjectOpened}>
          <Error text={addData?.error?.toString()} />
          <Center>
            <SegmentedControl
              onChange={setNetworkEvent}
              value={network}
              mt="xl"
              mb="xl"
              radius="xl"
              size="md"
              data={networks}
              classNames={classes}
            />
          </Center>
          <Group align="flex-end">
            <TextInput data-autofocus autoFocus onKeyDown={maybeSubmit} required sx={{ flex: 1 }} onChange={doSetProjectName} value={projectName} />
            <Button color={"green"} loading={addData.loading} onClick={doCreateProject}>Add</Button>
          </Group>
        </FocusTrap>
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
                    <th>Network</th>
                    <th>Used stats</th>
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