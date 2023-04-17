import { useState } from 'react';
import { createStyles, Navbar, Anchor, getStylesRef, rem } from '@mantine/core';
import { IconDatabaseImport, IconLogout } from '@tabler/icons';
import { useNavigate } from 'react-router-dom';
import { UserButton } from './UserButton';
import { useStore } from '../store';
import { Link } from 'react-router-dom';


const useStyles = createStyles((theme) => ({
  navbar: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.white,
  },

  title: {
    textTransform: 'uppercase',
    letterSpacing: rem(-0.25),
  },

  link: {
    ...theme.fn.focusStyles(),
    display: 'flex',
    alignItems: 'center',
    textDecoration: 'none',
    fontSize: theme.fontSizes.sm,
    color: theme.colorScheme === 'dark' ? theme.colors.dark[1] : theme.colors.gray[7],
    padding: `${theme.spacing.xs} ${theme.spacing.sm}`,
    borderRadius: theme.radius.sm,
    fontWeight: 500,

    '&:hover': {
      backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
      color: theme.colorScheme === 'dark' ? theme.white : theme.black,

      [`& .${getStylesRef('icon')}`]: {
        color: theme.colorScheme === 'dark' ? theme.white : theme.black,
      },
    },
  },

  linkIcon: {
    ref: getStylesRef('icon'),
    color: theme.colorScheme === 'dark' ? theme.colors.dark[2] : theme.colors.gray[6],
    marginRight: theme.spacing.sm,
  },

  linkActive: {
    '&, &:hover': {
      backgroundColor: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).background,
      color: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).color,
      [`& .${getStylesRef('icon')}`]: {
        color: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).color,
      },
    },
  },

  footer: {
    borderTop: `${rem(1)} solid ${
      theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]
    }`,
    paddingTop: theme.spacing.md,
  },
}));

const data = [
  { link: '/dashboard', label: 'Projects', icon: IconDatabaseImport },
];

export function NavbarSection() {
  const { classes, cx } = useStyles();
  const [active, setActive] = useState('Billing');
  const navigate = useNavigate();
  let { user } = useStore();

  if (!user.isLoading && !user.isLoggedIn) {
    navigate("/");
  }

  const signOut = () => {
    user.logOut();
    navigate("/");
  }

  const links = data.map((item) => (
    <Anchor
      component={Link}
      to={item.link}
      className={cx(classes.link, { [classes.linkActive]: item.label === active })}
      key={item.label}
      onClick={() => {
        setActive(item.label);
      }}
    >
      <item.icon className={classes.linkIcon} stroke={1.5} />
      <span>{item.label}</span>
    </Anchor>
  ));

  return (
    <Navbar width={{ sm: 300 }} p="md">
      <Navbar.Section>
        <UserButton
          image={user.props?.getImageUrl(80) || ""}
          name={user.props?.username || ""}
          email={user.props?.email || ""}
        />
      </Navbar.Section>

      <Navbar.Section grow>
        {links}
      </Navbar.Section>

      <Navbar.Section className={classes.footer}>
        <Anchor className={classes.link} onClick={signOut}>
          <IconLogout className={classes.linkIcon} stroke={1.5} />
          <span>Logout</span>
        </Anchor>
      </Navbar.Section>
    </Navbar>
  );
}