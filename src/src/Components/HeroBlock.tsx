import { createStyles, Title, Button, Group, Text, List, ThemeIcon, Anchor } from '@mantine/core';
import { IconCheck } from '@tabler/icons';
import graphqlLogo from '../assets/images/graphql.svg';
import tronLogo from '../assets/images/tron.svg';
import { Logo } from './Logo';


const useStyles = createStyles((theme) => ({
  inner: {
    display: 'flex',
    justifyContent: 'space-between',
    paddingTop: theme.spacing.xl * 4,
    paddingBottom: theme.spacing.xl * 4,
  },

  centerRow: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexDirection: "row"
  },

  centerColumn: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center"
  },

  smallTitle: {
    fontSize: "36px",
    fontWeight: "bold"
  },

  title: {
    color: theme.colorScheme === 'dark' ? theme.white : theme.black,
    fontFamily: `Greycliff CF, ${theme.fontFamily}`,
    fontSize: 44,
    lineHeight: 1.2,
    fontWeight: 900,

    [theme.fn.smallerThan('xs')]: {
      fontSize: 28,
    },
  },

  control: {
    [theme.fn.smallerThan('xs')]: {
      flex: 1,
    },
  },

  image: {
    flex: 1,

    [theme.fn.smallerThan('md')]: {
      display: 'none',
    },
  },

  highlight: {
    position: 'relative',
    backgroundColor: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).background,
    borderRadius: theme.radius.sm,
    padding: '4px 12px',
  },
}));

export function HeroBullets() {
  const { classes } = useStyles();
  return (
    <>
      <div className={classes.inner} style={{justifyContent: "center"}}>
        <div>
          <Title className={classes.title}>
            A <span className={classes.highlight}>modern</span>
            <Anchor href="https://graphql.org/" target={"_blank"}>Graphql</Anchor><br />
            api service for <Anchor href="https://tron.network/" target={"_blank"}>TRON</Anchor>.
          </Title>
          <Text color="dimmed" mt="md">
            Build fully functional accessible web applications faster than ever
          </Text>

          <br />
          <Title className={classes.title}>Advantages</Title>
          <List
            mt={30}
            spacing="sm"
            size="sm"
            icon={
              <ThemeIcon size={20} radius="xl">
                <IconCheck size={12} stroke={1.5} />
              </ThemeIcon>
            }
          >
            <List.Item>
              Describe what’s possible with a type system
            </List.Item>
            <List.Item>
              A query language for your API
            </List.Item>
            <List.Item>
              Get many resources in a single request
            </List.Item>
          </List>

          <Group mt={30}>
            <Button component="a" href="https://api.tronql.com/" radius="xl" size="md" className={classes.control}>
              Get started
            </Button>
          </Group>
        </div>
        <div className={classes.centerColumn}>
          <div className={classes.centerRow}>
            <img width={48} height={48} alt="Tron logo" src={tronLogo} />
            <span className={classes.smallTitle}>Tron</span>
          </div>
          <div className={classes.centerRow}>
            <span className={classes.smallTitle}>+</span>
          </div>
          <div className={classes.centerRow}>
            <img width={48} height={48} alt="Graphql logo" src={graphqlLogo} />
            <span className={classes.smallTitle}>Graphql</span>
          </div>
          <div className={classes.centerRow}>
            <span className={classes.smallTitle}>=</span>
          </div>
          <div className={classes.centerRow}>
            <Logo size={48} />
          </div>
        </div>
      </div>
    </>
  );
}