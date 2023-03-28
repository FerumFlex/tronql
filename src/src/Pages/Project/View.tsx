import { useState } from "react";
import { Prism } from '@mantine/prism';
import { Paper, Breadcrumbs, Text, Anchor, Title, ActionIcon, Group, Skeleton, TextInput, Loader, Card, SimpleGrid } from "@mantine/core";
import { useParams } from "react-router-dom";
import { IconPencil, IconCheck } from '@tabler/icons';
import { useQuery, useMutation } from "@apollo/client";
import { GET_PROJECT } from "../../graphql/queries";
import { EDIT_PROJECT } from "../../graphql/mutations";
import { Error } from "../../Components/Error";
import { ProjectStats } from "../../Components/Projects/ProjectStats";
import { ProjectInfo } from "../../Components/Projects/ProjectInfo";
import { Link } from "react-router-dom";
import { useStyles } from "../../styles";
import { DateTime } from "luxon";


export function ProjectViewPage () {
  const end = DateTime.now();
  let { projectId } = useParams();
  const { classes } = useStyles();
  const [newName, setNewName] = useState("");
  const [isEditing, setIsEditing] = useState(false);

  const [editProject, editData] = useMutation(EDIT_PROJECT, {
    refetchQueries: [
      {
        query: GET_PROJECT,
        variables: {
          projectId: parseInt(projectId || ""),
          begin: end.minus({ months: 1 }).toISODate() ,
          end: end.toISODate()
        }
      }
    ],
    onCompleted() {
      setNewName("");
      setIsEditing(false);
    }
  });

  const { loading, error, data } = useQuery(GET_PROJECT, {
    variables: {
      projectId: parseInt(projectId || ""),
      begin: end.minus({ months: 1 }).toISODate() ,
      end: end.toISODate()
    }
  });

  const onChangeInput = (e: any) => {
    setNewName(e.target.value);
  };

  const setEditing = () => {
    setNewName(data.project.name);
    setIsEditing(true);
  };

  const saveName = () => {
    editProject({
      variables: {
        projectId: parseInt(projectId || ""),
        name: newName
      }
    });
  };

  const maybeSubmit = (e: any) => {
    if (e.keyCode === 13) {
      saveName();
    }
  };

  const items = [
    <Anchor component={Link} to="/dashboard/" key={0}>
      Projects list
    </Anchor>,
    <Anchor component={Link} to={`/dashboard/project/${projectId}`} key={1}>
      View project
    </Anchor>,
  ];

  const url = "https://mainnet.tron.tronql.com/";
  let code = "";
  let graph = [];
  if (data) {
    code = `curl --location --request POST '${url}wallet/getnowblock' --header 'Authorization: ${data.project.token}'`;

    for (var i in data.getStats) {
      let row = data.getStats[i];
      graph.push({
        "x": row["date"].replace("T", " ").replace("+00:00", ".000"),
        "y": row["count"]
      })
    }
  }

  return (
    <>
      <Paper mb={20}>
        <Breadcrumbs separator="→" mt="xs">{items}</Breadcrumbs>
      </Paper>
      { loading ? (
        <Skeleton height={8} mt={6} radius="xl" />
      ) : (
        <>
          { error ? (
            <Error text={error?.toString()} />
          ) : (
            <>
              <Card withBorder p={10} radius="md">
                <Error text={editData.error?.toString()} />
                <Group>
                  { isEditing ? (
                    <>
                      <ActionIcon onClick={saveName}>
                        <IconCheck color={"green"} size={16} stroke={1.5} />
                      </ActionIcon>
                      <TextInput autoFocus={true} onKeyDown={maybeSubmit} value={newName} onChange={onChangeInput} />
                      { editData.loading && <Loader /> }
                    </>
                  ) : (
                    <>
                      <ActionIcon onClick={setEditing}>
                        <IconPencil size={16} stroke={1.5} />
                      </ActionIcon>
                      <Title size={30}>
                        {data.project.name}
                      </Title>
                    </>
                  )}
                </Group>
              </Card>
              <SimpleGrid cols={2} mb={20}>
                <Card withBorder mt={30} p={10} radius="md">
                  <ProjectInfo apiUrl={url} project={data.project} />
                </Card>
                <Card mt={30} p={10} radius="md">
                  <ProjectStats
                    title="Project stats"
                    completed={data.project.currentStats.total}
                    total={data.project.plan.requestsPerMonth}
                    rateLimit={data.project.plan.rateLimit}
                    ratePeriod={data.project.plan.ratePeriod}
                  />
                </Card>
              </SimpleGrid>
              <Card mb={20}>
                <Text fz="xl" className={classes.label}>
                  Example of request
                </Text>
                <Prism language="bash">{code}</Prism>
              </Card>
            </>
          )}
        </>
      )}
    </>
  )
}