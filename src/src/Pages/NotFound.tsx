import { Title, Text, Anchor, Container, Group } from '@mantine/core';
import { useStyles } from '../styles';


export function NotFoundPage() {
  const { classes } = useStyles();

  return (
    <Container className={classes.root}>
      <div className={classes.label}>404</div>
      <Title style={{textAlign: "center"}} className={classes.title}>You have found a secret place.</Title>
      <Text color="dimmed" size="lg" align="center" className={classes.description}>
        Unfortunately, this is only a 404 page. You may have mistyped the address, or the page has
        been moved to another URL.
      </Text>
      <Group position="center">
        <Anchor href="/" size="md">
          Take me back to home page
        </Anchor>
      </Group>
    </Container>
  );
}
