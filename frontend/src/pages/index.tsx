import styles from "src/app/page.module.css";
import Link from "next/link";

export default function Home() {
  return (
    // <Layout>
    <main className={styles.main}>
      <div className={styles.description}>
        <p>
          {/* Get started by working&nbsp; */}
          <code className={styles.code}>src/appage.tsx</code>
          <Link href="/about">About Page</Link>
        </p>
        <p>
          {/* Get started by working&nbsp; */}
          <code className={styles.code}>src/app/page.tsx</code>
          <Link href="/events">events</Link>
        </p>
      </div>
    </main>
    // </Layout>
  );
}
