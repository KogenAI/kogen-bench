import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from candidate_revision import read_head


class CandidateRevisionTests(unittest.TestCase):
    def make_repo(self, root):
        repo = Path(root) / 'repo'
        git = repo / '.git'
        (git / 'refs' / 'heads').mkdir(parents=True)
        return repo, git

    def test_reads_detached_and_loose_head(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, git = self.make_repo(temp)
            detached = 'a' * 40
            (git / 'HEAD').write_text(detached + '\n')
            self.assertEqual(read_head(repo), detached)
            (git / 'HEAD').write_text('ref: refs/heads/main\n')
            expected = 'b' * 40
            (git / 'refs' / 'heads' / 'main').write_text(expected + '\n')
            self.assertEqual(read_head(repo), expected)

    def test_reads_packed_ref(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, git = self.make_repo(temp)
            expected = 'c' * 40
            (git / 'HEAD').write_text('ref: refs/heads/main\n')
            (git / 'packed-refs').write_text('# pack-refs with: peeled fully-peeled\n'
                                             + expected + ' refs/heads/main\n')
            self.assertEqual(read_head(repo), expected)

    def test_rejects_symlink_and_fifo_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, git = self.make_repo(temp)
            target = Path(temp) / 'outside'
            target.write_text('d' * 40 + '\n')
            (git / 'HEAD').symlink_to(target)
            self.assertIsNone(read_head(repo))
            (git / 'HEAD').unlink()
            os.mkfifo(git / 'HEAD')
            self.assertIsNone(read_head(repo))

    def test_unsafe_loose_ref_does_not_fall_back_to_stale_packed_ref(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, git = self.make_repo(temp)
            (git / 'HEAD').write_text('ref: refs/heads/main\n')
            (git / 'packed-refs').write_text('e' * 40 + ' refs/heads/main\n')
            os.mkfifo(git / 'refs' / 'heads' / 'main')
            self.assertIsNone(read_head(repo))

    def test_rejects_symlinked_git_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / 'repo'
            repo.mkdir()
            external = Path(temp) / 'external-git'
            external.mkdir()
            (repo / '.git').symlink_to(external, target_is_directory=True)
            self.assertIsNone(read_head(repo))


if __name__ == '__main__':
    unittest.main()
