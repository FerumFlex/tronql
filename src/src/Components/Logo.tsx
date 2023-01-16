import { createStyles, Group, Anchor } from '@mantine/core';
import logo from '../assets/images/logo.svg';

const useStyles = createStyles((theme) => ({
  title: {
    fontWeight: 'bold',
    textTransform: 'uppercase',
    '&:hover': {
      textDecoration: 'none'
    }
  },
}));

export function Logo({ size } : {size: number}) {
  const { classes } = useStyles();
  return (
    <Group>
      <img src={logo} alt="logo" width={size} height={size} />
      <Anchor href="/" size="lg" className={classes.title}>Tronql</Anchor>
    </Group>
  );
}