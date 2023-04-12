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
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';


export function ProjectViewPage () {
  let { projectId } = useParams();
  const { classes } = useStyles();
  const [newName, setNewName] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const STATS_DAYS = 30;

  const now = DateTime.now().set({minute: 0, second: 0, millisecond: 0});
  const begin = now.minus({ day: 1 });
  const end = now;
  const begin2 = now.minus({ day: STATS_DAYS });
  let formatter = Intl.NumberFormat('en', { notation: 'compact' });

  const dateFormatter = (date: number) => {
    return DateTime.fromMillis(date).toFormat('D HH:mm');
  };
  const valueFormatter = (value: number) => {
    return formatter.format(value);
  };

  const [editProject, editData] = useMutation(EDIT_PROJECT, {
    refetchQueries: [
      {
        query: GET_PROJECT,
        variables: {
          projectId: parseInt(projectId || ""),
          begin: begin.toISO(),
          end: end.toISO(),
          begin2: begin2.toISO()
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
      begin: begin.toISO() ,
      end: end.toISO(),
      begin2: begin2.toISO()
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

  const domain = "mainnet.tron.tronql.com";
  let code = "";
  let code2 = "";
  let graph = [];
  let graphDay = [];
  if (data) {
    code = `curl --location --request POST 'https://${domain}/wallet/getnowblock' --header 'Authorization: ${data.project.token}'`;
    code2 = `curl --location --request POST 'https://${data.project.token}.${domain}/wallet/getnowblock'`;

    for (let row of data.getStats) {
      graph.push({
        "name": DateTime.fromISO(row["date"]).toMillis(),
        "count": row["count"]
      })
    }
    for (let row of data.dayStats) {
      graphDay.push({
        "name": DateTime.fromISO(row["date"]).toMillis(),
        "count": row["count"]
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
                  <ProjectInfo apiUrl={`https://${domain}/`} project={data.project} />
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
                <Text fz="xl" mb={30} className={classes.label}>
                  Example of request
                </Text>
                <Prism mb={30} language="bash">{code}</Prism>
                <Text mb={30} fz="xl" className={classes.label}>
                  Or another variant. Using token in domain
                </Text>
                <Prism language="bash">{code2}</Prism>
              </Card>
              <Card mb={20}>
                <Text fz="xl" mb={30} className={classes.label}>
                  Stats for last 24 hours
                </Text>
                <ResponsiveContainer height={200}>
                  <LineChart data={graph}>
                    <CartesianGrid strokeDasharray="1 5" />
                    <XAxis dataKey="name" tickFormatter={dateFormatter} type="number" domain={[begin.toMillis(), end.toMillis()]} />
                    <YAxis tickFormatter={valueFormatter} />
                    <Tooltip labelFormatter={dateFormatter} />
                    <Line type="monotone" dataKey="count" stroke="#82ca9d" />
                  </LineChart>
                </ResponsiveContainer>
              </Card>
              <Card mb={20}>
                <Text fz="xl" mb={30} className={classes.label}>
                  Stats for last {STATS_DAYS} days
                </Text>
                <ResponsiveContainer height={200}>
                  <LineChart data={graphDay}>
                    <CartesianGrid strokeDasharray="1 5" />
                    <XAxis dataKey="name" tickFormatter={dateFormatter} type="number" domain={[begin.toMillis(), end.toMillis()]} />
                    <YAxis tickFormatter={valueFormatter} />
                    <Tooltip labelFormatter={dateFormatter} />
                    <Line type="monotone" dataKey="count" stroke="#82ca9d" />
                  </LineChart>
                </ResponsiveContainer>
              </Card>
            </>
          )}
        </>
      )}
    </>
  )
}