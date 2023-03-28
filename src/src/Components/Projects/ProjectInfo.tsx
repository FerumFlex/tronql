import { Badge, Card, Text } from "@mantine/core";
import { useStyles } from "../../styles";

export function ProjectInfo({ project, apiUrl }: {project: any, apiUrl: string}) {
  const { classes } = useStyles();

  return (
    <Card withBorder p="xl" radius="md" className={classes.card}>
      <Text fz="xl" className={classes.label}>
        Credentials
      </Text>
      <div>
        <Badge>url</Badge>: {apiUrl}
      </div>
      <div>
        <Badge>token</Badge>: {project.token}
      </div>
    </Card>
  )
}